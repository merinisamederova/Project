const API = "http://127.0.0.1:5000/api/recipes";


let editingId = null;

async function loadRecipes() {
    const search = document.getElementById('search').value;
    const category = document.getElementById('categoryFilter').value;

    let url = API;
    const params = new URLSearchParams();
    if (search) params.append('q', search);
    if (category) params.append('category', category);

    if (params.toString()) url += "?" + params.toString();

    const resp = await fetch(url);
    const recipes = await resp.json();

    const list = document.getElementById('list');

    list.innerHTML = recipes.map(recipe => `
        <div class="recipe">
            <div class="recipe-header">
                ${recipe.image 
                    ? `<img src="${recipe.image}" class="recipe-image" alt="${recipe.title}">`
                    : `<div class="recipe-image" style="background:#ccc;display:flex;align-items:center;justify-content:center;">No Image</div>`}
                
                <div class="recipe-content">
                    <h3>${recipe.title}</h3>
                    <p><strong>Category:</strong> ${recipe.category}</p>
                    <p><strong>Author:</strong> ${recipe.author}</p>
                    <p><strong>Cooking Time:</strong> ${recipe.cook_time} minutes</p>
                    <p><strong>Rating:</strong> ${recipe.rating}/5</p>
                    ${recipe.favorite ? "<p>⭐ Favorite</p>" : ""}
                </div>
            </div>

            <p><strong>Ingredients:</strong></p>
            <ul>${recipe.ingredients.map(i => `<li>${i}</li>`).join("")}</ul>

            <p><strong>Instructions:</strong> ${recipe.instructions}</p>

            <button onclick="editRecipe(${recipe.id})" class="btn">Edit</button>
            <button onclick="deleteRecipe(${recipe.id})" class="btn">Delete</button>
        </div>
    `).join('');
}

async function editRecipe(id) {
    const resp = await fetch(`${API}/${id}`);
    const recipe = await resp.json();

    editingId = id;

    document.getElementById("rid").value = id;
    document.getElementById("title").value = recipe.title;
    document.getElementById("category").value = recipe.category;
    document.getElementById("author").value = recipe.author;
    document.getElementById("cook_time").value = recipe.cook_time;
    document.getElementById("ingredients").value = recipe.ingredients.join("\n");
    document.getElementById("instructions").value = recipe.instructions;
    document.getElementById("favorite").checked = recipe.favorite;

    document.getElementById("formTitle").innerText = "Edit Recipe";
    document.getElementById("formArea").style.display = "block";
}

async function deleteRecipe(id) {
    if (!confirm("Delete this recipe?")) return;

    await fetch(`${API}/${id}`, { method: "DELETE" });
    loadRecipes();
}

document.getElementById("recipeForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        title: document.getElementById("title").value,
        category: document.getElementById("category").value,
        author: document.getElementById("author").value,
        cook_time: parseInt(document.getElementById("cook_time").value),
        ingredients: document.getElementById("ingredients").value.split("\n"),
        instructions: document.getElementById("instructions").value,
        favorite: document.getElementById("favorite").checked
    };

    if (editingId) {
        await fetch(`${API}/${editingId}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
    } else {
        await fetch(API, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
    }

    document.getElementById("formArea").style.display = "none";
    editingId = null;
    loadRecipes();
});

document.getElementById("btnSearch").onclick = loadRecipes;

document.getElementById("search").addEventListener("keypress", e => {
    if (e.key === "Enter") loadRecipes();
});

document.getElementById("categoryFilter").addEventListener("change", loadRecipes);

document.getElementById("btnNew").onclick = () => {
    editingId = null;
    document.getElementById("recipeForm").reset();
    document.getElementById("formTitle").innerText = "Add Recipe";
    document.getElementById("formArea").style.display = "block";
};

document.getElementById("btnCancel").onclick = () =>
    document.getElementById("formArea").style.display = "none";

loadRecipes();
