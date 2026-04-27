    {% if products %}
        {% for product in products %}
        <p>{{ product['name'] }} — Aisle {{ product['aisle_number'] }} — {{ product['shelf'] }}</p>
        {% endfor %}
    {% else %}
        <p>No products yet!</p>
    {% endif %}
    </div>
    the above code is for showing all the products in admin dashboard...