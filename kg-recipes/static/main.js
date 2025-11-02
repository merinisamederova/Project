// main.js
let editingId = null;

async function loadRecipes() {
    const search = document.getElementById('search').value;
    const category = document.getElementById('categoryFilter').value;
    
    let url = '/api/recipes';
    const params = new URLSearchParams();
    if (search) params.append('q', search);
    if (category) params.append('category', category);
    if (params.toString()) url += '?' + params.toString();

    const resp = await fetch(url);
    const recipes = await resp.json();
    
    const list = document.getElementById('list');
    list.innerHTML = recipes.map(recipe => `
        <div class="recipe">
            <div class="recipe-header">
                ${recipe.image ? `<img src="${recipe.image}" class="recipe-image" alt="${recipe.title}">` : '<div class="recipe-image" style="background:#ccc;display:flex;align-items:center;justify-content:center;color:#666;">No Image</div>'}
                <div class="recipe-content">
                    <h3>${recipe.title}</h3>
                    <p><strong>Category:</strong> ${recipe.category}</p>
                    <p><strong>Author:</strong> ${recipe.author}</p>
                    <p><strong>Cooking Time:</strong> ${recipe.cook_time} minutes</p>
                    <p><strong>Rating:</strong> ${recipe.rating}/5</p>
                    ${recipe.favorite ? '<p>⭐ Favorite</p>' : ''}
                </div>
            </div>
            <p><strong>Ingredients:</strong></p>
            <ul>
                ${recipe.ingredients.map(ing => `<li>${ing}</li>`).join('')}
            </ul>
            <p><strong>Instructions:</strong> ${recipe.instructions}</p>
            <button onclick="editRecipe(${recipe.id})" class="btn">Edit</button>
            <button onclick="deleteRecipe(${recipe.id})" class="btn">Delete</button>
        </div>
    `).join('');
}


//document.getElementById('btnSearch').addEventListener('click', loadRecipes);
//document.getElementById('search').addEventListener('keypress', (e) => {
    //if (e.key === 'Enter') loadRecipes();
//});
//document.getElementById('categoryFilter').addEventListener('change', loadRecipes);


loadRecipes();