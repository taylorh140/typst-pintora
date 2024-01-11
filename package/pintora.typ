#import "@preview/jogs:0.2.1": compile-js, call-js-function

#let pintora-src = read("./pintora.js")
#let pintora-bytecode = compile-js(pintora-src)

#let render(src, ..args) = {
  let result = call-js-function(pintora-bytecode, "PintoraRender", src)
  result = ```<svg version="1.1" xmlns="http://www.w3.org/2000/svg"```.text + result.slice(4,)

  image.decode(result, ..args)
}


#show raw.where(lang: "pintora"): it => render(it.text)

```pintora
mindmap
@param layoutDirection TB
@param {
  l1NodeBgColor   #2B7A5D
  l1NodeTextColor #fff
  l2NodeBgColor   #26946C
  l2NodeTextColor #fff
  nodeBgColor     #67B599
  textColor       #fff

+ UML Diagrams
++ Behavior Diagrams
+++ Sequence Diagram
+++ State Diagram
+++ Activity Diagram
++ Structural Diagrams
+++ Class Diagram
+++ Component Diagram
```