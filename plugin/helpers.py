import json
from pathlib import Path
from typing import Union

def json_load_comments(path: Path):
    lines = list()
    with open(path, "r") as f:
        for line in f:
            if line.strip().startswith("//"):
                continue

            lines.append(line)
    
    content = "".join(lines)
    return json.loads(content)

class Results:
    def __init__(self) -> None:
        self._results = list()

    @property
    def results(self):
        return self._results

    def add_item(self, title:str, subtitle:str='', icon:str=None, method:Union[str, callable]=None, parameters:list=None, score:int=0, context:list=None, **kwargs):
        item = {
            "Title": title,
            "SubTitle": subtitle,
            "IcoPath": icon or "",
            "Score": score,
            "JsonRPCAction": {},
            "ContextData": context
        }

        if method:
            item['JsonRPCAction']['method'] = getattr(method, "__name__", method)
            item['JsonRPCAction']['parameters'] = parameters or [""]
        
        self._results.append(item)