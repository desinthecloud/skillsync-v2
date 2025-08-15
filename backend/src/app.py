import json, os, uuid
from datetime import datetime, timezone
import boto3
from boto3.dynamodb.conditions import Key

TABLE_NAME = os.environ["TABLE_NAME"]
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def _resp(status, body):
    return {"statusCode": status,
            "headers": {"Access-Control-Allow-Origin": ALLOWED_ORIGINS,
                        "Access-Control-Allow-Headers": "*",
                        "Access-Control-Allow-Methods": "*",
                        "Content-Type": "application/json"},
            "body": json.dumps(body)}

def _now(): return datetime.now(timezone.utc).isoformat()

def lambda_handler(event, context):
    m = event.get("requestContext",{}).get("http",{}).get("method","")
    p = event.get("rawPath","")
    q = event.get("queryStringParameters") or {}
    path = event.get("pathParameters") or {}
    try: data = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError: data = {}

    if p=="/health" and m=="GET": return _resp(200, {"ok":True,"service":"skillsync","time":_now()})
    if p=="/skills" and m=="GET":
        uid=q.get("userId"); 
        if not uid: return _resp(400, {"error":"Missing userId"})
        return _resp(200, {"items": _list(uid)})
    if p=="/skills" and m=="POST":
        uid=data.get("userId"); name=data.get("name")
        if not uid or not name: return _resp(400, {"error":"userId and name required"})
        return _resp(201, _create(uid, name, data.get("level",""), data.get("notes","")))
    if p.startswith("/skills/") and m=="PUT":
        sid=path.get("id"); uid=data.get("userId")
        if not uid or not sid: return _resp(400, {"error":"userId and id required"})
        upd={k:v for k,v in data.items() if k in ["name","level","notes"]}
        if not upd: return _resp(400, {"error":"Provide at least one of: name, level, notes"})
        return _resp(200, _update(uid, sid, upd))
    if p.startswith("/skills/") and m=="DELETE":
        sid=path.get("id"); uid=(q.get("userId") if q else None)
        if not uid or not sid: return _resp(400, {"error":"userId and id required"})
        _delete(uid,sid); return _resp(204, {})
    return _resp(404, {"error":"Not found"})

def _create(uid,name,level,notes):
    now=_now(); item={"userId":uid,"skillId":str(uuid.uuid4()),"name":name,"level":level,"notes":notes,"createdAt":now,"updatedAt":now}
    table.put_item(Item=item); return item
def _list(uid): return table.query(KeyConditionExpression=Key("userId").eq(uid)).get("Items",[])
def _update(uid,sid,upd):
    names={}; vals={}; sets=[]
    for k,v in upd.items(): names[f"#_{k}"]=k; vals[f":{k}"]=v; sets.append(f"#_{k} = :{k}")
    names["#_updatedAt"]="updatedAt"; vals[":updatedAt"]=_now(); sets.append("#_updatedAt = :updatedAt")
    r=table.update_item(Key={"userId":uid,"skillId":sid}, UpdateExpression="SET "+", ".join(sets),
                        ExpressionAttributeNames=names, ExpressionAttributeValues=vals, ReturnValues="ALL_NEW")
    return r["Attributes"]
def _delete(uid,sid): table.delete_item(Key={"userId":uid,"skillId":sid}); return True
