console.log('hi')

const newTaskForm = document.getElementById('new-task-form');
const taskInput = document.getElementById('ntask-input');
const newTDList = document.getElementById('new-tdlist');
const taskTemplate = document.getElementById('template-task').content;

const fragment = document.createDocumentFragment();

let tasks = {};

newTaskForm.addEventListener('submit', e =>{
  e.preventDefault();
  // console.log(taskInput.value);
  setTask(e);
})

const setTask  = e =>{
  if (taskInput.value.trim() === ''){
    console.log('Empty form');
    return
  }

  const ntask = {
    id:Date.now(), 
    text: taskInput.value,
    isDone: false,
  }
  tasks[ntask.id] = ntask;
  newTaskForm.reset();
  taskInput.focus();
  displayTasks();
}

const displayTasks = () =>{
  newTDList.innerHTML = '';
  // console.log(taskTemplate)
  Object.values(tasks).forEach(task => {
    const clone = taskTemplate.cloneNode(true);
    clone.querySelector('label').textContent = task.text;
    fragment.appendChild(clone);
  } )
  newTDList.appendChild(fragment);
}