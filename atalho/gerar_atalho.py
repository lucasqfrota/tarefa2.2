"""Gera o atalho 'Baixar video X' (.shortcut, nao assinado)."""
import plistlib, uuid

def u(): return str(uuid.uuid4()).upper()

def ref_input():
    return {"Value": {"Type": "ExtensionInput"}, "WFSerializationType": "WFTextTokenAttachment"}
def ref_out(uid, name):
    return {"Value": {"Type": "ActionOutput", "OutputUUID": uid, "OutputName": name},
            "WFSerializationType": "WFTextTokenAttachment"}
def ref_var(name):
    return {"Value": {"Type": "Variable", "VariableName": name}, "WFSerializationType": "WFTextTokenAttachment"}
def token_str(att):
    return {"Value": {"string": "￼", "attachmentsByRange": {"{0, 1}": att["Value"]}},
            "WFSerializationType": "WFTextTokenString"}
def act(ident, **p): return {"WFWorkflowActionIdentifier": ident, "WFWorkflowActionParameters": p}

r1, r2, dl, gv, dl2, grp = u(), u(), u(), u(), u(), u()
actions = [
    act("is.workflow.actions.text.replace", UUID=r1, WFInput=token_str(ref_input()),
        WFReplaceTextFind=r"(twitter|x)\.com", WFReplaceTextReplace="api.vxtwitter.com",
        WFReplaceTextRegularExpression=True),
    act("is.workflow.actions.text.replace", UUID=r2, WFInput=token_str(ref_out(r1, "Texto Atualizado")),
        WFReplaceTextFind=r"\?.*", WFReplaceTextReplace="", WFReplaceTextRegularExpression=True),
    act("is.workflow.actions.downloadurl", UUID=dl, WFURL=token_str(ref_out(r2, "Texto Atualizado"))),
    act("is.workflow.actions.getvalueforkey", UUID=gv, WFDictionaryKey="mediaURLs",
        WFGetDictionaryValueType="Value", WFInput=ref_out(dl, "Conteúdo do URL")),
    act("is.workflow.actions.repeat.each", GroupingIdentifier=grp, WFControlFlowMode=0,
        WFInput=ref_out(gv, "Valor do Dicionário")),
    act("is.workflow.actions.downloadurl", UUID=dl2, WFURL=token_str(ref_var("Repeat Item"))),
    act("is.workflow.actions.savetocameraroll", WFInput=ref_out(dl2, "Conteúdo do URL")),
    act("is.workflow.actions.repeat.each", GroupingIdentifier=grp, WFControlFlowMode=2),
    act("is.workflow.actions.notification", WFNotificationActionTitle="Baixar vídeo X",
        WFNotificationActionBody="Vídeo salvo na galeria ✅"),
]
wf = {
    "WFWorkflowActions": actions,
    "WFWorkflowClientVersion": "2302.0.4",
    "WFWorkflowMinimumClientVersion": 900,
    "WFWorkflowMinimumClientVersionString": "900",
    "WFWorkflowIcon": {"WFWorkflowIconStartColor": 255, "WFWorkflowIconGlyphNumber": 59511},
    "WFWorkflowImportQuestions": [],
    "WFWorkflowInputContentItemClasses": ["WFURLContentItem", "WFStringContentItem"],
    "WFWorkflowTypes": ["ActionExtension"],
    "WFWorkflowHasShortcutInputVariables": True,
    "WFWorkflowNoInputBehavior": {"Name": "WFWorkflowNoInputBehaviorGetClipboard", "Parameters": {}},
    "WFQuickActionSurfaces": [],
}
with open("Baixar video X (nao assinado).shortcut", "wb") as f:
    plistlib.dump(wf, f, fmt=plistlib.FMT_BINARY)
print("ok")
