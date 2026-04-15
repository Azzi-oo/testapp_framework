# Test Cases for automationteststore.com

## Test Case 1: Filter Categories — Sorting by Name and Price

**Test Object:** Category page with at least 4 products (Apparel & accessories — path=68, 8 products)

**Preconditions:**
- Browser is open
- User navigates to the category page: `https://automationteststore.com/index.php?rt=product/category&path=68`

### Test Case 1.1: Sort products by Name A-Z

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open the category page | Category page loads with product grid displayed |
| 2 | Locate the "Sort By" dropdown (`#sort`) | Dropdown is visible and accessible |
| 3 | Select "Name A - Z" option (`pd.name-ASC`) | Page reloads with products sorted |
| 4 | Collect all product names from the grid (`.prdocutname`) | Product names are collected |
| 5 | Verify the product names are in ascending alphabetical order | Names list equals sorted(names, case-insensitive) |

### Test Case 1.2: Sort products by Name Z-A

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open the category page | Category page loads with product grid displayed |
| 2 | Select "Name Z - A" option (`pd.name-DESC`) from the Sort By dropdown | Page reloads with products sorted |
| 3 | Collect all product names from the grid | Product names are collected |
| 4 | Verify the product names are in descending alphabetical order | Names list equals sorted(names, reverse=True, case-insensitive) |

### Test Case 1.3: Sort products by Price Low > High

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open the category page | Category page loads with product grid displayed |
| 2 | Select "Price Low > High" option (`p.price-ASC`) from the Sort By dropdown | Page reloads with products sorted |
| 3 | Collect all product prices from the grid (`.oneprice` or `.pricenew`) | Prices are collected as float values |
| 4 | Verify the prices are in ascending numerical order | Prices list equals sorted(prices) |

### Test Case 1.4: Sort products by Price High > Low

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open the category page | Category page loads with product grid displayed |
| 2 | Select "Price High > Low" option (`p.price-DESC`) from the Sort By dropdown | Page reloads with products sorted |
| 3 | Collect all product prices from the grid | Prices are collected as float values |
| 4 | Verify the prices are in descending numerical order | Prices list equals sorted(prices, reverse=True) |

---

## Test Case 2: Search Results and Cart

**Test Object:** Search functionality and cart operations

**Preconditions:**
- Browser is open
- Cart is empty

### Test Case 2.1: Search, sort, add to cart, and verify total after doubling cheapest

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open the main page `https://automationteststore.com/` | Main page loads |
| 2 | Enter "shirt" in the search field (`#filter_keyword`) and submit | Search results page loads |
| 3 | Verify search results are displayed | At least 2 products are shown |
| 4 | Select "Name A - Z" from the Sort By dropdown (`#sort`) | Products are sorted by name ascending |
| 5 | Identify the 2nd and 3rd products from the sorted results | Products are identified by index |
| 6 | Click on the 2nd product to open its product page | Product page loads |
| 7 | Set a random quantity (2-5) in the quantity input (`#product_quantity`) | Quantity is set |
| 8 | Click "Add to Cart" button | Product added to cart, confirmation displayed |
| 9 | Navigate back to search results | Search results page loads |
| 10 | Click on the 3rd product to open its product page | Product page loads |
| 11 | Set a random quantity (2-5) in the quantity input | Quantity is set |
| 12 | Click "Add to Cart" button | Product added to cart |
| 13 | Navigate to the cart page (`checkout/cart`) | Cart page loads with 2 items |
| 14 | Identify the cheapest product in the cart by comparing unit prices | Cheapest product found |
| 15 | Double the quantity of the cheapest product (update quantity field, click Update) | Quantity is updated |
| 16 | Verify the cart total matches the sum of (unit_price * quantity) for all items | Cart total equals calculated total |

---

## Test Case 3: Cart — Add Random Products and Remove Even-Numbered

**Test Object:** Cart manipulation with product addition and removal

**Preconditions:**
- Browser is open
- Cart is empty

### Test Case 3.1: Add 5 random products, remove even-numbered, verify total

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open the main page `https://automationteststore.com/` | Main page loads with product sections |
| 2 | Collect all products with "Add to Cart" buttons on the main page | Products with `.productcart` buttons found (products with `href="#"` — i.e., those that can be directly added) |
| 3 | Randomly select 5 unique products from the available list | 5 products selected |
| 4 | For each of the 5 products: click on the product to open its page | Product page loads |
| 5 | Set a random quantity (1-5) in the quantity input (`#product_quantity`) | Quantity is set |
| 6 | Click "Add to Cart" button | Product is added to cart |
| 7 | Navigate back to the main page | Main page loads |
| 8 | After adding all 5 products, navigate to the cart page | Cart page loads with 5 items |
| 9 | Verify all 5 products are present in the cart table | All products are listed |
| 10 | Identify products at even positions (2nd, 4th) in the cart table | Even-numbered rows identified |
| 11 | Remove all even-numbered products by clicking the remove button | Products are removed |
| 12 | Verify that only odd-numbered products remain (1st, 3rd, 5th) | 3 products remain in cart |
| 13 | Calculate expected total: sum of (unit_price * quantity) for remaining products | Expected total calculated |
| 14 | Verify the displayed cart total matches the expected total | Cart total equals calculated total |
