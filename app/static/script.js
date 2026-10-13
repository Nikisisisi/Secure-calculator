async function calculate(operation) {
    const resultElement = document.getElementById("result");
    const aInput = document.getElementById("a");
    const bInput = document.getElementById("b");

    const requiresB = operation !== "factorial" && operation !== "sqrt";

    const aText = aInput.value.trim();
    const bText = bInput.value.trim();

    if (aText === "" || (requiresB && bText === "")) {
        resultElement.textContent = "Ошибка: заполните необходимые поля.";
        return;
    }

    const a = Number(aText);
    const b = Number(bText);

    if (!Number.isFinite(a) || (requiresB && !Number.isFinite(b))) {
        resultElement.textContent = "Ошибка: введите корректные числа.";
        return;
    }

    let requestBody;

    if (operation === "factorial") {
        requestBody = { n: a };
    } else if (operation === "sqrt") {
        requestBody = { a: a };
    } else {
        requestBody = { a: a, b: b };
    }

    try {
        const response = await fetch(`/calculate/${operation}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestBody)
        });

        const data = await response.json();

        if (response.ok) {
            const result = operation === "factorial"
                && typeof data.result_exact === "string"
                    ? data.result_exact
                    : data.result;

            resultElement.textContent = "Результат: " + result;
        } else {

            const errorMessage = Array.isArray(data.detail)
                ? data.detail.map(error => error.msg).join("; ")
                : (data.detail || "Неизвестная ошибка сервера");

            resultElement.textContent = "Ошибка: " + errorMessage;
        }
    } catch (error) {
        resultElement.textContent =
            "Ошибка: не удалось получить ответ сервера.";
    }
}
async function loadVersion() {
    const versionElement = document.getElementById("version");

    try {
        const response = await fetch("/");

        if (!response.ok) {
            throw new Error("Version request failed");
        }

        const data = await response.json();

        versionElement.textContent =
            "Secure Calculator API v" + data.version;
    } catch (error) {
        versionElement.textContent = "Версия API недоступна";
    }
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
