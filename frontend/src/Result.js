import axios from "axios";
import React from "react";
import Rowcol from "./Rowcol";
import {type} from "@testing-library/user-event/dist/type";

class Result extends React.Component {
    constructor(props) {
        super(props);
        console.log(props)
        this.state = {
            message: " ",
            status: -1,
            x: Array(),
            max: -1,
            success: false,
            is_received: false,
            details: {
                format: Array(),
                d_set: Array(),
                oi_set: Array(),

            }
        }
        this.init(props)
        this.askForDetails = this.askForDetails.bind(this);

    }

    init(props) {
        this.state.message = props.state.message
        this.state.status = props.state.status
        this.state.x = props.state.x
        this.state.max = props.state.max
        this.state.success = props.state.success
    }


    askForDetails(event) {
        let that = this;
        axios.post('http://127.0.0.1:5000/simplex/details', {
            'target': this.props.target,
            'matrix': this.props.matrix
        })
            .then(function (responses) {

                that.setState({
                    details: {
                        format: responses.data.format,
                        d_set: responses.data.d_set,
                        oi_set: responses.data.oi_set,
                    }
                }, () => {
                    that.setState({is_received: true})
                })
            })
            .catch(function (error) {
                console.log(error)
            })
    }

    render() {
        let format, iter_process, oi_process;
        if (this.state.is_received) {
            console.log(this.state.details, this.state.details.format)
            let init_params = Array.from(this.state.details.format[this.props.equ_number])
            init_params.shift()
            init_params.shift()
            format =
                <table>
                    <tbody>
                    <tr>
                        <td colSpan="3">Cj</td>
                        {init_params.map(
                            (element, index) =>
                                <td key={"format_t" + index}>{element}</td>
                        )}
                    </tr>
                    <tr>
                        <td>Cb</td>
                        <td>Xb</td>
                        <td>b</td>
                        {init_params.map(
                            (element, index) =>
                                index < init_params.length && <td key={"format_x" + index}>X{index}</td>
                        )}
                        <td key={"theta"}>theta</td>
                    </tr>
                    {this.state.details.format.map(
                        (element, index1) =>
                            index1 < this.props.equ_number ?
                                <tr>
                                    <td>0</td>
                                    <td>X{element[0]}</td>
                                    {
                                        element.map(
                                            (number, index2) =>
                                                index2 > 0 &&
                                                <td key={"format_e" + index1 + index2}>{number}
                                                </td>
                                        )
                                    }
                                </tr> :
                                <tr>
                                    <td colSpan="2">Cj-Zj</td>
                                    {
                                        element.map(
                                            (number, index2) =>
                                                index2 > 0 && <td key={"format_e" + index1 + index2}>{number}</td>
                                        )
                                    }
                                </tr>
                    )}
                    </tbody>
                </table>

            iter_process =
                this.state.details.d_set.map(
                    (arr2, index) =>
                        <div>
                            <br/>
                            第{index + 1}次迭代
                            <table>
                                <tbody>
                                <tr>
                                    <td colSpan="3">Cj</td>
                                    {init_params.map(
                                        (element, index) =>
                                            <td key={"format_t" + index}>{element}</td>
                                    )}
                                </tr>
                                <tr>
                                    <td>Cb</td>
                                    <td>Xb</td>
                                    <td>b</td>
                                    {init_params.map(
                                        (element, index) =>
                                            index < init_params.length && <td key={"format_x" + index}>X{index}</td>
                                    )}
                                    <td key={"theta"}>theta</td>
                                </tr>
                                {arr2.map(
                                    (element, index1) =>
                                        index1 < this.props.equ_number ?
                                            <tr>
                                                <td>{init_params[element[0]]}</td>
                                                <td>X{element[0]}</td>
                                                {
                                                    element.map(
                                                        (number, index2) =>
                                                            index2 > 0 &&
                                                            <td key={"format_e" + index1 + index2}>{number}</td>
                                                    )
                                                }
                                            </tr> :
                                            <tr>
                                                <td colSpan="2">Cj-Zj</td>
                                                {
                                                    element.map(
                                                        (number, index2) =>
                                                            index2 > 0 &&
                                                            <td key={"format_e" + index1 + index2}>{number}</td>
                                                    )
                                                }
                                            </tr>
                                )}
                                </tbody>
                            </table>
                        </div>
                )

        }

        return (
            <div>
                message: {this.state.message}
                <br/>
                x : {this.state.x}
                <br/>
                max : {this.state.max}
                <br/>
                success: {this.state.success.toString()}
                <br/>
                {/*如果结果为success 既可以迭代成功 选择访问*/}
                {
                    this.state.success &&
                    (!this.state.is_received ?
                        <div>
                            <button type="submit" onClick={this.askForDetails}>迭代过程</button>
                        </div> : <div>
                            {/*    显示详细结果*/}
                            标准化单纯形法表
                            <br/>
                            {format}
                            迭代过程
                            <br/>
                            {iter_process}
                        </div>)
                }
            </div>
        )
    }
}

export default Result;