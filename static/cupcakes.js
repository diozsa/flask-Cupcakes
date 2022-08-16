// Generate the <ul> with <li> of all cakes

function createLI(cupcake) {
    // returns HTML with the cupcake info
    return ` <div data-id=${cupcake.id}>
                <img style="width: 200px" src="${cupcake.image}"
                <li>
                    <b class="text-info">
                    ${cupcake.flavor} | ${cupcake.size} | ${cupcake.rating}
                    </b>
                    <button class=" delete btn btn-sm btn-danger">Delete</button>
                </li>
             </div>
    `;
}

// populate home page with cupcakes

async function populateCupcakes() {
    const resp = await axios.get("http://127.0.0.1:5000/api/cupcakes");
    for (let cupcake of resp.data.cupcakes) {
        let newCupcake = createLI(cupcake)
        $("#cupcakes-ul").append(newCupcake)
    }    
}

// form handler for adding new cupcake


$("#cupcake-form").on("submit", async function (e) {
    e.preventDefault();
  
    let flavor = $("#flavor").val();
    let size = $("#size").val();
    let rating = $("#rating").val();
    let image = $("#image").val();

    const resp = await axios.post("http://127.0.0.1:5000/api/cupcakes", 
    {flavor, size, rating, image});
    
    let newCupcake = $(createLI(resp.data.cupcake));
    $("#cupcakes-ul").append(newCupcake);
    $("#cupcake-form").trigger("reset");
  });


  // delete a cupcake - delete button handler

$("#cupcakes-ul").on("click", ".delete", async function (e) {
    e.preventDefault();
    let $cupcake = $(e.target).closest("div");
    let id = $cupcake.attr("data-id");
    
    await axios.delete(`http://127.0.0.1:5000/api/cupcakes/${id}`);
    $cupcake.remove();
  });


populateCupcakes();

