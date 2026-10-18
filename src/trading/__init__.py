class Trade:
    def __init__(self, trader1, trader2, t1profile, t2profile):
        self.t1 = trader1
        self.t2 = trader2

        self.t1prof = t1profile
        self.t2prof = t2profile

        self.t1ready = False
        self.t2ready = False

        self.slots={
            self.t1.id: [],
            self.t2.id: []
        }
        self.ids={}

        self._has_values = 1

    def has_values(self):
        return self._has_values==1

    def send_items(self):
        for prof, target_prof, slot in \
            zip(
                [self.t1prof, self.t2prof],
                [self.t2prof, self.t1prof],
                self.slots.values()
            ):
            for item in slot:
                match item.item_type:
                    case "uma":
                        uma_entry = target_prof["inventory"]["umas"].setdefault(item.item_id, [0,0])
                        uma_entry[0]+=item.amount
                        prof["inventory"]["umas"][item.item_id][0]-=item.amount
                    case "carats":
                        target_prof["stats"]["carats"]+=item.amount
                        prof["stats"]["carats"]-=item.amount

    def set_amount(self, slot, iid, amount, override=False):
        if str(slot)+iid in self.ids:
            trade_item = self.ids[str(slot)+iid]
            old, new = trade_item.change_amount(amount, override=override)
        else:
            item = TradeItem(iid, amount)
            self.slots[slot].append(
                item
            )
            self.ids[str(slot)+iid]=item
            old, new = -9999, amount
        if new == old: return new
        if new>0 and "???" not in iid:
            self._has_values+=1
        else:
            self._has_values-=1
        return new
    def set_carats(self, user, amount):
        self.set_amount(user.id, "carats", amount, override=True)

    def add_uma(self, user, uma_name="???"):
        return self.set_amount(user.id, "uma_"+uma_name, 1)

    def remove_unknown_item(self, slot, iid):
        key = str(slot)+iid+"_???"
        if key not in self.ids:
            return
        item = self.ids[key]
        if item.change_amount(-1)[0]<=0:
            self.slots[slot].remove(item)
            del self.ids[key]
    def remove_item(self, slot, iid):
        if str(slot)+iid in self.ids:
            self.slots[slot].remove(self.ids[str(slot)+iid])
            del self.ids[str(slot)+iid]

    def refresh_slots(self, slot):
        for i in self.slots[slot]:
            i.amount=0

class TradeItem:
    def __init__(self, item_type, amount=0):
        data = item_type.split("_")
        self.item_type = data[0]
        self.item_id   = data[1] if len(data)==2 else None
        self.amount    = amount

    def change_amount(self, amount, override=False):
        old = self.amount
        if override:
            self.amount = amount
        else:
            self.amount += amount
        return old, self.amount
