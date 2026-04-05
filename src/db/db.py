from collections import UserDict
import discord
import pickle

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
        

    @classmethod         
    async def load(cls, bot, fp):
        with open(fp, 'rb') as f:
            data = pickle.load(f)
        _data = await desafenize(
            bot, data
        )

        return cls(_data)
