import  quickjs
from jsmin import jsmin
from pathlib import Path

TS1 = """
sequenceDiagram
  title: Sequence Diagram Example
  autonumber
  participant [<actor> User]
  User->>Pintora: Draw me a sequence diagram（with DSL）
  activate Pintora
  Pintora->>Pintora: Parse DSL, draw diagram
  alt DSL is correct
    Pintora->>User: Return the drawn diagram
  else DSL is incorrect
    Pintora->>User: Return error message
  end
  deactivate Pintora
  @note left of Pintora
  Different output formats according to render targets
  1. In browser side. output SVG or Canvas
  2. In Node.js side. output PNG file
  @end_note
"""

TS2 = """
mindmap
@param layoutDirection TB
@param {
  l1NodeBgColor   #2B7A5D
  l1NodeTextColor #fff
  l2NodeBgColor   #26946C
  l2NodeTextColor #fff
  nodeBgColor     #67B599
  textColor       #fff
}
+ UML Diagrams
++ Behavior Diagrams
+++ Sequence Diagram
+++ State Diagram
+++ Activity Diagram
++ Structural Diagrams
+++ Class Diagram
+++ Component Diagram
"""


TS3= """
componentDiagram
  title: Component Diagram Example
  package "@pintora/core" {
    () GraphicsIR
    () IRenderer
    () IDiagram
    [Diagram Registry] as registry
  }
  package "@pintora/diagrams" {
    [...Multiple Diagrams...] as diagrams
    [diagrams]
    [diagrams] --> IDiagram : implements
  }
  package "@pintora/renderer" {
    () "render()" as renderFn
    [SVGRender]
    [CanvasRender]
    [SVGRender] --> IRenderer : implements
    [CanvasRender] --> IRenderer : implements
    IRenderer ..> GraphicsIR : accepts
  }
  package "@pintora/standalone" {
    [standalone]
  }
  [IDiagram] --> GraphicsIR : generate
  [standalone] --> registry : register all of @pintora/diagrams
  [@pintora/standalone] --> [@pintora/diagrams] : import
  [standalone] --> renderFn : call with GraphicsIR

"""


qj = quickjs.Context()
file = []
def qjeval(instr):
    qj.eval(instr)
    file.append(instr)


pintora = Path('runtime.esm.js')
encoding = Path('encoding.js')
encodingIdx = Path('encoding-indexes.js')



qjeval('''
class ConsoleStub {
  constructor() {
    this.logHistory   = [];
    this.errorHistory = [];
    this.warnHistory  = [];
  }

  log(...args) {
    const message = args.join(' ');
    this.logHistory.push(message);
  }

  error(...args) {
    const message = args.join(' ');
    this.errorHistory.push(message);
  }

  warn(...args) {
    const message = args.join(' ');
    this.warnHistory.push(message);
  }
}

var console = new ConsoleStub();

    ''')

import re

qjeval(encodingIdx.read_text(encoding="UTF-8"))
qjeval(encoding.read_text(encoding="UTF-8"))


QJSFIXED = re.sub(r"export\s*\{.*\}","//EXPORTS arn't SUPPORTED",
                pintora.read_text(encoding="UTF-8")
                  .replace("import.meta.url",'""'),
                flags = re.MULTILINE|re.DOTALL)

# print("\n".join(QJSFIXED.split("\n")[63152:63158]))
qjeval(QJSFIXED)





qjeval("""
    var document = new Document()
    var csrc = document.createElement("div")
    csrc.dataset=[];
    var rslt = document.createElement("svg")

    csrc.dataset['renderer']


    function PintoraRender(InputString) {

        console = new ConsoleStub()
        csrc.innerText=InputString
        pintoraStandalone.renderContentOf(csrc,{resultContainer:rslt})

        if (rslt.innerHTML===""){
        errorString = '\\n ' + String(console.warnHistory.slice(-1))
        throw new Error(errorString);
        }
        rslt.firstChild.setAttribute("xmlns","http://www.w3.org/2000/svg")
        return rslt.innerHTML;
    }

    """)
Path("package/pintora.js").write_text(jsmin("\n".join(file)),encoding="UTF-8")



Render=qj.eval("PintoraRender")

print(Render(TS2))

print(qj.eval(""))


# print(Render(TS3))

# print(qj.eval("pintoraStandalone.renderTo(randStr,{container:rslt,config:null})"))

# #look at logs and errors:
# print(qj.eval("console.logHistory.join()"))
# print(qj.eval("console.warnHistory.join()"))
# print(qj.eval("console.errorHistory.join()"))

# # get output
# print(qj.eval("rslt.innerHTML"))
# Path("output.svg").write_text(qj.eval("rslt.innerHTML"),encoding="UTF-8")
