Naming
======
'**naming**' is a simple drop-in python library to solve and manage names by
setting configurable rules in the form of a naming convention.


### Quick start

```python
import naming as n

# let's add some fields
n.add_field("side", {"l": "L", "r": "R", "m": "M"}, default="m")
n.add_field("description", "")
n.add_field("enumerator", 0, padding=3)
n.add_field("category", {"ch": "CHAR", "cam": "CAM", "root": "ROOT"}, default="char")
n.add_field("type", {"geo": "GEO", "jnt": "JNT", "loc": "LOC", "rig":"RIG"}, default="loc")

# setup a new profile
profile = n.add_profile("DG")
profile.set_fields("category", "description", "enumerator", "side", "type")
n.set_active_profile("DG"):

# save your session in order to make it persistent
n.save()


# let's solve some names
n.solve("test")                 # CHAR_test_000_M_loc
n.solve("test", 7)              # CHAR_test_007_M_loc
n.solve("test", "root", "jnt")  # ROOT_test_000_L_jnt

# or we can make use of fancy context managers
with n.defaults(side="r", description="test", type="geo"):
	n.solve()   # CHAR_test_000_R_GEO
    n.solve(1)  # CHAR_test_001_R_GEO
    n.solve(2)  # CHAR_test_002_R_GEO

    # you can also override defaults per call
	n.solve("m")  # CHAR_test_000_M_GEO
	n.solve()     # CHAR_test_000_R_GEO


# what about decoding names?
n.unsolve("CHAR_test_000_R_GEO")
# {"category": "ch", "description": "test", "enumerator": 0, "side": "r", "type": "geo"}

n.unsolve("ROOT_test_000_M_JNT").get("side")  # "m"
n.unsolve("ROOT_test_000_M_JNT")["type"]      # "jnt"
```

# Docs

Check out the documentation at [cesarsaez.me/naming](http://cesarsaez.me/naming)
