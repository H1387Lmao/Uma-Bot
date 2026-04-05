from collections import UserDict
import discord
import pickle, re

def safenize(old, step=0):
    _new={}
    for k, v in old.items():
        if isinstance(v, dict):
            _new[k]=safenize(v)
        elif isinstance(v, discord.User):
            _new[k]={
                "__type__": "dsc.user",
                "v": v.id
            }
            continue
        _new[k]=v
    return _new

async def desafenize(bot, data):
    _new = {}
    for k, v in data.items():
        if not isinstance(v, dict):
            _new[k]=v
            continue
        if "__type__" not in v:
            _new[k]=await desafenize(bot, v)
            continue
        _type = v["__type__"]

        if _type.startswith("dsc."):
            v = await getattr(bot, f"sfetch_{_type.removeprefix("dsc.")}")(v["id"])
            _new[k]=v
            continue
        _new[k]=v
    return _new

class Database(UserDict):
    def __init__(self, data=None):
        super().__init__(data)
    def __setitem__(self, key, value):
        super().__setitem__(str(key), value)
    def save(self, fp):
        _data = safenize(self.data)
        with open(fp, 'wb') as f:
            pickle.dump(_data, f, pickle.HIGHEST_PROTOCOL)
            
    def temp_load(self, fp):
        if fp.exists():
            with open(fp, 'rb') as f:
                self.data = pickle.load(f)

    def query(self, condition: str) -> dict | None:
        cond = self._parse(condition)
        return self._search(self.data, cond, "", 0)

    def _parse(self, c: str) -> dict:
        patterns = [
            (r'^KEY\s*==\s*"([^"]+)"$',           lambda m: {"type": "key_eq",       "key": m[1]}),
            (r'^VALUE\s*>\s*(\d+(?:\.\d+)?)$',    lambda m: {"type": "val_gt",       "n": float(m[1])}),
            (r'^VALUE\s*<\s*(\d+(?:\.\d+)?)$',    lambda m: {"type": "val_lt",       "n": float(m[1])}),
            (r'^VALUE\s*==\s*"([^"]+)"$',          lambda m: {"type": "val_eq_s",     "s": m[1]}),
            (r'^VALUE\s*==\s*(true|false)$',       lambda m: {"type": "val_eq_b",     "b": m[1] == "true"}, re.IGNORECASE),
            (r'^VALUE\s*==\s*(\d+(?:\.\d+)?)$',   lambda m: {"type": "val_eq_n",     "n": float(m[1])}),
            (r'^VALUE\s+CONTAINS\s+"([^"]+)"$',    lambda m: {"type": "val_contains", "s": m[1]}, re.IGNORECASE),
            (r'^\.(\w+)\s*==\s*"([^"]+)"$',        lambda m: {"type": "field_eq_s",   "field": m[1], "s": m[2]}),
            (r'^\.(\w+)\s*==\s*(true|false)$',     lambda m: {"type": "field_eq_b",   "field": m[1], "b": m[2] == "true"}, re.IGNORECASE),
            (r'^\.(\w+)\s*==\s*(\d+(?:\.\d+)?)$', lambda m: {"type": "field_eq_n",   "field": m[1], "n": float(m[2])}),
        ]
        for entry in patterns:
            flags = entry[2] if len(entry) == 3 else 0
            m = re.match(entry[0], c.strip(), flags)
            if m:
                return entry[1](m)
        raise ValueError(f"Unrecognised condition: {c}")

    def _matches(self, cond: dict, key, value) -> bool:
        t = cond["type"]
        if t == "key_eq":      return str(key) == cond["key"]
        if t == "val_gt":      return isinstance(value, (int, float)) and value > cond["n"]
        if t == "val_lt":      return isinstance(value, (int, float)) and value < cond["n"]
        if t == "val_eq_s":    return value == cond["s"]
        if t == "val_eq_b":    return value == cond["b"]
        if t == "val_eq_n":    return value == cond["n"]
        if t == "val_contains":return isinstance(value, str) and cond["s"] in value
        if t in ("field_eq_s", "field_eq_b", "field_eq_n"):
            if not isinstance(value, dict):
                return False
            fv = value.get(cond["field"])
            if t == "field_eq_s": return fv == cond["s"]
            if t == "field_eq_b": return fv == cond["b"]
            if t == "field_eq_n": return fv == cond["n"]
        return False

    def _search(self, node, cond: dict, path: str, depth: int) -> dict | None:
        if depth > 50:
            return None
        if isinstance(node, list):
            for i, item in enumerate(node):
                result = self._search(item, cond, f"{path}[{i}]", depth + 1)
                if result:
                    return result
            return None
        if isinstance(node, dict):
            for key, value in node.items():
                current_path = f"{path}.{key}" if path else key
                if self._matches(cond, key, value):
                    return {"path": current_path, "depth": depth, "value": value}
                if isinstance(value, (dict, list)):
                    result = self._search(value, cond, current_path, depth + 1)
                    if result:
                        return result
        return None
    @classmethod         
    async def load(cls, bot, fp):
        with open(fp, 'rb') as f:
            data = pickle.load(f)
        _data = await desafenize(
            bot, data
        )

        return cls(_data)
