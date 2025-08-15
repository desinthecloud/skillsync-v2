async function api(path, options = {}) {
  const base = window.API_BASE_URL || "";
  if (!base) { alert("API_BASE_URL not set. Edit frontend/config.js after deploying the backend."); throw new Error("Missing API_BASE_URL"); }
  const res = await fetch(base + path, { headers: { "Content-Type": "application/json" }, ...options });
  if (!res.ok) { const text = await res.text(); throw new Error(`HTTP ${res.status}: ${text}`); }
  return res.status === 204 ? null : res.json();
}
function el(tag, attrs = {}, children = []) { const e=document.createElement(tag); Object.entries(attrs).forEach(([k,v])=>e[k]=v); children.forEach(c=>e.appendChild(typeof c==="string"?document.createTextNode(c):c)); return e; }
async function refreshList() {
  const userId=document.getElementById("listUserId").value.trim(); if(!userId){alert("Enter your User ID to list skills.");return;}
  const data=await api(`/skills?userId=${encodeURIComponent(userId)}`); const ul=document.getElementById("skills"); ul.innerHTML="";
  for(const it of data.items){
    const li=el("li",{},[
      el("div",{className:"row"},[ el("strong",{},[it.name]), el("span",{className:"badge"},[it.level||""]), el("span",{className:"small"},[it.notes||""]) ]),
      el("div",{className:"row"},[
        el("span",{className:"action",onclick:async()=>{ const name=prompt("New name:",it.name)||it.name; const level=prompt("New level (Beginner|Intermediate|Advanced):",it.level||"")||it.level||""; const notes=prompt("New notes:",it.notes||"")||it.notes||""; const uid=document.getElementById("listUserId").value.trim(); await api(`/skills/${it.skillId}`,{method:"PUT",body:JSON.stringify({userId:uid,name,level,notes})}); await refreshList(); }},["Edit"]),
        el("span",{className:"action danger",onclick:async()=>{ const uid=document.getElementById("listUserId").value.trim(); if(!confirm("Delete this skill?"))return; await api(`/skills/${it.skillId}?userId=${encodeURIComponent(uid)}`,{method:"DELETE"}); await refreshList(); }},["Delete"]),
      ]),
    ]); ul.appendChild(li);
  }
}
document.getElementById("refresh").addEventListener("click", refreshList);
document.getElementById("add-form").addEventListener("submit", async (e)=>{ e.preventDefault(); const userId=document.getElementById("userId").value.trim(); const name=document.getElementById("skillName").value.trim(); const level=document.getElementById("skillLevel").value; const notes=document.getElementById("skillNotes").value.trim(); await api("/skills",{method:"POST",body:JSON.stringify({userId,name,level,notes})}); document.getElementById("skillName").value=""; document.getElementById("skillLevel").value=""; document.getElementById("skillNotes").value=""; document.getElementById("listUserId").value=userId; await refreshList(); });
