import React, {useState, useEffect} from 'react';
import TodoDataService from '../services/todos';
import { Link } from 'react-router-dom';

const TodosList = props => {
    const [todos, setTodos] = useState([]);
}

useEffect(() =>{
    retrieveTodos();
}, [props.token]);

const retrieveTodos = () => {
  TodoDataService.getAll(props.token)
    .then(response => {
    setTodos(response.data);
    })
    .catch( e => {
     console.log(e);
    });
}

export default TodosList;