import React from "react";
import './App.css';
import axios from "axios";
import Result from './Result'
import {Link} from "react-router-dom";


class Rowcol extends React.Component {
    constructor() {
        super();
        this.state = {
            v_number: "2",
            equ_number: "4",
            is_input: false
        }

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState(
            {
                [event.target.name]: event.target.value
            })

    }

    handleSubmit(event) {
        this.setState({is_input: true},)
        event.preventDefault();
    }


    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <div>
                    变量个数：<input type="number" name="v_number" value={this.state.v_number} onChange={this.handleChange}/>
                </div>
                <div>
                    约束个数：<input type="number" name="equ_number" value={this.state.equ_number}
                                onChange={this.handleChange}/>
                </div>

                {this.state.is_input ?
                    <div><InputBox v_number={this.state.v_number} equ_number={this.state.equ_number}/></div> :
                    <button type="submit">点击提交</button>}

            </form>
        )
    }
}

class InputBox extends React.Component {
    constructor(props) {
        console.log("input box constructor")
        super(props);
        this.state = {
            target: Array(),
            matrix: Array(new Array(props.v_number + 1)),
            is_submit: false,
            result: {
                message: " ",
                status: -1,
                x: Array(),
                max: -1,
                success: false
            }
        }
        this.init(props)
        this.handleTargetChange = this.handleTargetChange.bind(this);
        this.handleMatrixChange = this.handleMatrixChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    init(props) {
        // 给target和matrix赋值
/*        for (let i = 0; i < props.v_number; i++) {
            this.state.target[i] = null
            for (let j = 0; j < props.equ_number; j++) {
                let tmp = new Array(props.v_number + 1)
                for (let k = 0; k <= props.v_number; k++) {
                    tmp[k] = null
                }
                this.state.matrix[j] = tmp
            }
        }*/
        this.state.target = [2, 3]
        this.state.matrix = [
            [2, 2, 12],
            [1, 2, 8],
            [4, 0, 16],
            [0, 4, 12]
        ]
    }

    handleTargetChange(event) {
        let tmp = this.state.target
        tmp[event.target.name] = event.target.value
        this.setState({target: tmp})
    }

    handleMatrixChange(event) {
        let index1 = event.target.name.split(" ")[0]
        let index2 = event.target.name.split(" ")[1]
        let tmp = this.state.matrix
        tmp[index1][index2] = event.target.value
        this.setState({matrix: tmp})

    }

    handleSubmit(event) {

        if (this.state.matrix.filter((e) => {
            return e == null
        }).length != 0 || this.state.target.filter((e) => {
            return e == null
        }).length != 0) {
            alert("not finish")
            return null;
        }
        let that = this;
        axios.post('http://127.0.0.1:5000/simplex/direct', {
            'target': this.state.target,
            'matrix': this.state.matrix
        })
            .then(function (responses) {
                console.log(responses)
                that.setState({
                    result: {
                        message: responses.data.message,
                        status: responses.data.status,
                        x: responses.data.x,
                        max: responses.data.max,
                        success: responses.data.success
                    }
                })
            })
            .catch(function (error) {
                console.log(error)
            })
        this.setState({is_submit: true})
        event.preventDefault()


    }

    render() {
        let targetList = this.state.target.map((number, index) =>
            <span key={"target" + index}>
                <input type="number" name={index} onChange={this.handleTargetChange} value={this.state.target[index]}/>
                x{index} {index != this.props.v_number - 1 && <span>+</span>}
            </span>
        )

        let matrixList = this.state.matrix.map(
            (element, index1) =>
                <div key={"line" + index1}>
                    {element.map(
                        (number, index2) =>
                            index2 <= this.props.v_number - 1 ?
                                <span key={"matrix" + index1 + index2}>
                                    <input type="number" name={(index1 + " " + index2).toString()}
                                           onChange={this.handleMatrixChange}
                                           value={this.state.matrix[index1][index2]}/>
                                    x{index2} {index2 != this.props.v_number - 1 && <span>+</span>}
                                </span> :
                                <span key={"matrix" + index1 + index2}>
                                    <span> {"<".toString()}= </span>
                                    <input type="number" name={index1 + " " + index2}
                                           onChange={this.handleMatrixChange}
                                           value={this.state.matrix[index1][index2]}/>
                                </span>
                    )}
                </div>
        )

        return (
            <div>
                {/*基础组件 target matrix输入框*/}
                max=
                {targetList}
                <div key="matrix">
                    {matrixList}
                </div>
                {
                    !this.state.is_submit && <button type="submit" onClick={this.handleSubmit}>提交</button>
                }
                <button type="submit" onClick={() => window.location.reload()}>重新输入</button>
                {/*如果有结果 显示结果*/}
                {this.state.result.status != -1 &&
                <Result state={this.state.result} target={this.state.target} matrix={this.state.matrix}
                        v_number={this.props.v_number} equ_number={this.props.equ_number}/>}
            </div>
        );

    }


}

export default Rowcol;