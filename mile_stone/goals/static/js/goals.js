document.addEventListener("click", async (e) => {
    const box = e.target.closest(".box");
    if (box) {
        const goalId = box.dataset.goal;
        const value = box.dataset.value;

        const response = await fetch("/api/update-progress/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                goal_id: goalId,
                value: value
            })
        });

        const data = await response.json();

        if (data.success) {
            updateUI(goalId, data.current_value);
        }

        return;
    }

    //parent checkbox logic
    const parentBox = e.target.closest(".parent-box");
    if (!parentBox) return;

    const goalId = parentBox.dataset.goal;
    const isComplete = parentBox.dataset.complete === "1";

    // find target
    const goalBoxes = document.querySelectorAll(`[data-goal='${goalId}']`);
    const target = goalBoxes.length;

    let newValue;

    if (isComplete) {
        parentBox.classList.remove("filled");
        parentBox.dataset.complete = "0";
        newValue = 0; // clear all
    } else {
        parentBox.classList.add("filled");
        parentBox.dataset.complete = "1";
        newValue = target; // fill all
    }

    
    updateUI(goalId, newValue);

    //send to backend
    await fetch("/api/update-progress/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            goal_id: goalId,
            value: newValue
        })
    });
});

// update visual boxes without reload
function updateUI(goalId, value) {
    const current = Number(value);

    const boxes = document.querySelectorAll(`[data-goal='${goalId}']`);

    // update all boxes
    boxes.forEach(box => {
        const boxValue = Number(box.dataset.value);

        if (boxValue <= current) {
            if (!box.classList.contains("filled")) {
                box.classList.add("filled");
                box.classList.add("animate");
            }
        } else {
            box.classList.remove("filled");
            box.classList.remove("animate");
        }
    });

    // update parent boxes
    const parentBox = document.querySelector(`.parent-box[data-goal='${goalId}']`);
    if (parentBox) {
        const total = boxes.length;

        if (current >= total) {
            parentBox.classList.add("filled");
            parentBox.dataset.complete = "1";
        } else {
            parentBox.classList.remove("filled");
            parentBox.dataset.complete = "0";
        }
    }
}
// CSRF helper (Django requirement)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}