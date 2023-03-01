import logo from './logo.svg';
import './App.css';
import {BrowserRouter as Router, Routes, Route, Link, BrowserRouter} from "react-router-dom";
import Rowcol from "./Rowcol";
import React from "react";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/simplex" element={<Rowcol/>}/>
                <Route path="/" element={<Home/>}/>
            </Routes>

        </BrowserRouter>
    );
}

function Home() {
    return (
        <nav>
            <Link to="/simplex"> simplex</Link>
        </nav>
    )
}


export default App;
