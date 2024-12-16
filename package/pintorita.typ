#import "@preview/jogs:0.2.3": compile-js, call-js-function

#let pintora-src = read("./pintora.js")
#let pintora-bytecode = compile-js(pintora-src)

#let getWidth(svg-output, factor) = {
  if (factor == none) {
    return auto
  }

  let svg-width = svg-output.find(regex("width=\"(\d+)")).find(regex("\d+"))
  let width = int(svg-width) * factor * 1pt
  return width
}

#let render(src, ..args) = {
  let named-args = args.named()

  let factor = named-args.at("factor",default:none)
  let style = named-args.at("style",default:"larkLight")
  let font = named-args.at("font",default:"Arial")

  let svg-output = call-js-function(pintora-bytecode, "PintoraRender", src, style, font)

  let width = getWidth(svg-output, factor)

  image.decode(
    svg-output, 
    width: width,
  )
}

#let render-svg(src, ..args) = {
  // style: ["default", "larkLight", "larkDark", "dark"]
  let named-args = args.named()
  let factor = named-args.at("factor",default:none)
  let style = named-args.at("style",default:"larkLight")
  let font = named-args.at("font",default:"Arial")
  let svg-output = call-js-function(pintora-bytecode, "PintoraRender", src, style, font)


  svg-output
}
