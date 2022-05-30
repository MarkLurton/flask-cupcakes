const $cupcakes = $(".cupcakes");
const $form = $(".add-cupcake-form");
const $flavor = $("#flavor");
const $size = $("#size");
const $rating = $("#rating");
const $image = $("#image");

async function get_cupcakes() {
  const cupcakes = await axios.get("/api/cupcakes");
  return cupcakes.data.cupcakes;
}

async function render_cupcakes() {
  const cupcakes = await get_cupcakes();
  for (let cupcake of cupcakes) {
    console.log(cupcake);
    const $cupcake = $(`<div data-id=${cupcake["id"]}></div>`);
    const $img = $(`<img class='w-25 h-25'src=${cupcake["image"]} />`);
    const $rating = $(`<p>Rating: ${cupcake["rating"]}</p>`);
    const $size = $(`<p>Size: ${cupcake["size"]}</p>`);
    const $flavor = $(`<p>Flavor: ${cupcake["flavor"]}</p>`);

    $cupcake.append($img, $flavor, $size, $rating);
    $cupcakes.append($cupcake);
  }
}

render_cupcakes();

$form.on("submit", async function (evt) {
  evt.preventDefault();
  const data = {
    flavor: $flavor.val(),
    size: $size.val(),
    rating: $rating.val(),
    image: $image.val(),
  };
  await axios.post("/api/cupcakes", data);
  location.reload();
});
