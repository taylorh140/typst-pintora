#import "@preview/jogs:0.2.3": compile-js, call-js-function

#let pintora-src = read("./pintora.js")
#let pintora-bytecode = compile-js(pintora-src)

#let getNewWidth(svg-output, factor, width) = {
  if (factor == none) {
    return width
  }

  let svg-width = svg-output.find(regex("width=\"(\d+)")).find(regex("\d+"))
  let width = int(svg-width) * factor * 1pt
  return width
}

#let render(
  src,
  factor: none,
  style: "larkLight",
  font: "Arial",
  width: auto,
  ..args,
) = {
  let named-args = args.named()

  let svg-output = call-js-function(pintora-bytecode, "PintoraRender", src, style, font)

  let newWidth = getNewWidth(svg-output, factor, width)

  image.decode(
    svg-output,
    width: newWidth,
    ..args,
  )
}

#let render-svg(
  src,
  style: "larkLight",
  font: "Arial",
) = {
  // style: ["default", "larkLight", "larkDark", "dark"]
  let svg-output = call-js-function(pintora-bytecode, "PintoraRender", src, style, font)

  svg-output
}
