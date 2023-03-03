import logo from './logo.svg';
import './App.css';
import {BrowserRouter as Router, Routes, Route, Link, BrowserRouter} from "react-router-dom";
import Rowcol from "./Rowcol";
import React from "react";
import PathPlaningPage from "./PathPlanning";
import MaxStream from "./MaxStream";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/simplex" element={<Rowcol/>}/>
                <Route path="/" element={<Home/>}/>
                <Route path="/path" element={<PathPlaningPage/>}/>
                <Route path="/maxflow" element={<MaxStream/>}/>
            </Routes>

        </BrowserRouter>
    );
}

function Home() {
    return (
        <nav>
            <div>
                <Link to="/simplex"> simplex</Link>
            </div>
            <div>
                <Link to="/path">path planing</Link>
            </div>
        </nav>
    )
}


export default App;
