async function calculate(operation) {

    const a =
        Number(document.getElementById("a").value);

    const b =
        Number(document.getElementById("b").value);

        let requestBody;

    if (operation === "factorial") {
        requestBody = { n: a };
    } else if (operation === "sqrt") {
        requestBody = { a: a };
    } else {
        requestBody = { a: a, b: b };
    }


    const response = await fetch(
        `/calculate/${operation}`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(requestBody)
        }
    );


    const data = await response.json();


    if (response.ok) {

        document.getElementById("result").textContent =
            "Результат: " + data.result;

    } else {

    const errorMessage =
        Array.isArray(data.detail)
            ? data.detail.map(error => error.msg).join("; ")
            : data.detail;

    document.getElementById("result").textContent =
        "Ошибка: " + errorMessage;

    }
}
async function loadVersion() {

    const response = await fetch("/");
    const data = await response.json();

    document.getElementById("version").textContent =
        "Secure Calculator API v" + data.version;
}

document.querySelectorAll("[data-operation]").forEach((button) => {
    button.addEventListener("click", () => {
        calculate(button.dataset.operation);
    });
});

let activeInput = document.getElementById("a");

document.querySelectorAll("#a, #b").forEach((input) => {
    input.addEventListener("focus", () => {
        activeInput = input;
    });
});

document.querySelectorAll("[data-constant]").forEach((button) => {
    button.addEventListener("click", () => {
        const value =
            button.dataset.constant === "pi"
                ? Math.PI
                : Math.E;

        activeInput.value = String(value);
        activeInput.focus();
    });
});

loadVersion();
