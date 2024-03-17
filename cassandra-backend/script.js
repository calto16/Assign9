document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('todo-form');
    const taskInput = document.getElementById('task-input');
    const todoList = document.getElementById('todo-list');

    // Function to fetch and display tasks from the backend
    function fetchTasks() {
        fetch('http://127.0.0.1:5000/todo') // Updated URL
            .then(response => response.json())
            .then(data => {
                todoList.innerHTML = ''; // Clear previous list
                data.forEach(task => {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <span>${task.task}</span>
                        <button class="delete-btn" data-id="${task.id}">Delete</button>
                    `;
                    todoList.appendChild(li);
                });
            })
            .catch(error => console.error('Error fetching tasks:', error));
    }

    // Fetch tasks on page load
    fetchTasks();

    // Add task event listener
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        const taskText = taskInput.value.trim();
        if (taskText !== '') {
            fetch('http://127.0.0.1:5000/todo', { // Updated URL
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ task: taskText }),
            })
            .then(response => response.json())
            .then(() => {
                taskInput.value = ''; // Clear input field
                fetchTasks(); // Refresh tasks list
            })
            .catch(error => console.error('Error adding task:', error));
        }
    });

    // Delete task event listener (event delegation)
    todoList.addEventListener('click', function (event) {
        if (event.target.classList.contains('delete-btn')) {
            const taskId = event.target.getAttribute('data-id');
            fetch(`http://127.0.0.1:5000/todo/${taskId}`, { // Updated URL
                method: 'DELETE',
            })
            .then(() => fetchTasks()) // Refresh tasks list after deletion
            .catch(error => console.error('Error deleting task:', error));
        }
    });
});
