import sys
from pathlib import Path
sys.path.insert(0, str(Path("4-SYSTEM/Skills/library-upload/scripts").resolve()))
from webuddhist import envs, text as T
from webuddhist.api import Client
from webuddhist.ledger import Ledger
env = envs.get("prod")
ctx = T.Ctx(env=env, client=Client(env), ledger=Ledger(env.name, "texts"))
for it in T.assess_all("text", sys.argv[1:], ctx, progress=False):
    L, B = it.live_content or "", it.p["edition"]["content"]
    print(it.key, "live **:", L.count("**"), " built **:", B.count("**"))
