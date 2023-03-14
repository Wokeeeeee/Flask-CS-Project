import logo from './logo.svg';
import './App.css';
import {BrowserRouter as Router, Routes, Route, Link, BrowserRouter} from "react-router-dom";
import Rowcol from "./Rowcol";
import React from "react";
import PathPlaningPage from "./PathPlanning";
import MaxStream from "./MaxStream";
import Transportation from "./Transportation"
import CounterPage from "./Counter"

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/simplex" element={<Rowcol/>}/>
                <Route path="/" element={<Home/>}/>
                <Route path="/path" element={<PathPlaningPage/>}/>
                <Route path="/maxflow" element={<MaxStream/>}/>
                <Route path="/transportation" element={<Transportation/>}/>
                <Route path="/counter" element={<CounterPage/>}/> </Routes>

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
            <div>
                <Link to="/maxflow">max flow</Link>
            </div>
            <div>
                <Link to="/transportation">transportation</Link>
            </div>
            <div>
                <Link to="/counter">cpunter</Link>
            </div>
        </nav>
    )
}


export default App;
