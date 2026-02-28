let balance = 10000;

let stocks = {
    tech: { name: "TechStar", price: 500, quantity: 0 },
    food: { name: "FoodHub", price: 300, quantity: 0 },
    study: { name: "StudyPro", price: 200, quantity: 0 }
};

function buyStock(type) {
    let stock = stocks[type];

    if (balance < stock.price) {
        document.getElementById("result").innerText = "❌ Not enough balance!";
        return;
    }

    balance -= stock.price;
    stock.quantity++;
    document.getElementById("result").innerText =
        "✅ Bought 1 share of " + stock.name;

    updateUI();
}

function sellStock(type) {
    let stock = stocks[type];

    if (stock.quantity <= 0) {
        document.getElementById("result").innerText =
            "❌ You don't own this stock!";
        return;
    }

    balance += stock.price;
    stock.quantity--;
    document.getElementById("result").innerText =
        "💰 Sold 1 share of " + stock.name;

    updateUI();
}

function updatePrices() {
    for (let key in stocks) {
        let change = Math.floor(Math.random() * 101) - 50;
        stocks[key].price += change;

        if (stocks[key].price < 50) {
            stocks[key].price = 50;
        }
    }

    document.getElementById("result").innerText =
        "📊 Market prices updated!";

    updateUI();
}

function updateUI() {
    document.getElementById("balance").innerText = balance;

    document.getElementById("techPrice").innerText = stocks.tech.price;
    document.getElementById("foodPrice").innerText = stocks.food.price;
    document.getElementById("studyPrice").innerText = stocks.study.price;

    let portfolioList = document.getElementById("portfolio");
    portfolioList.innerHTML = "";

    let totalWealth = balance;

    for (let key in stocks) {
        let stock = stocks[key];

        if (stock.quantity > 0) {
            let value = stock.quantity * stock.price;
            totalWealth += value;

            let li = document.createElement("li");
            li.innerText =
                stock.name +
                " - Shares: " +
                stock.quantity +
                " | Value: ₹" +
                value;

            portfolioList.appendChild(li);
        }
    }

    document.getElementById("totalWealth").innerText = totalWealth;
}