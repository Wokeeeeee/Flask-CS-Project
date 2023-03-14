import React from "react";
import axios from "axios";


class Transportation extends React.Component {
    render() {
        return <InputBox/>
    }
}

class InputBox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            produce_num: 3,
            sale_num: 4,
            matrix: Array(),
            show_input: false,
            is_received: false,
            c: {
                success: false,
                message: "",
                minn_cost: -1,
                matrix: null
            }
        }

        this.handleNumberChange = this.handleNumberChange.bind(this)
        this.handleNumberSubmit = this.handleNumberSubmit.bind(this)
        this.handleMatrixChange = this.handleMatrixChange.bind(this)
        this.upload = this.upload.bind(this)
    }

    handleNumberChange(event) {
        this.setState(
            {
                [event.target.name]: event.target.value
            }, () => console.log(this.state))
    }

    handleNumberSubmit() {
        let tmp = [
            [4, 12, 4, 11, 16],
            [2, 10, 3, 9, 10],
            [8, 5, 11, 6, 22],
            [8, 14, 12, 14, 0]
        ]
        this.setState({
            matrix: tmp
        }, () => {
            console.log(this.state)
            this.setState({show_input: true})
        })
    }

    handleMatrixChange(event) {
        let index1 = event.target.name.split(" ")[0]
        let index2 = event.target.name.split(" ")[1]
        let tmp = this.state.matrix
        tmp[index1][index2] = event.target.value
        this.setState({matrix: tmp}, () => console.log(this.state))
    }

    upload() {
        let that = this
        if (this.state.matrix.filter(
            (line) => {
                return line.filter((e) => {
                    return e === ""
                }).length > 0
            }).length > 0 && this.state.des === "" && this.state.src === ""
        ) {
            alert("not finish")
            return null;
        } else {
            console.log("发送请求")
            axios.post('http://127.0.0.1:5000/transportation', {
                'matrix': this.state.matrix
            })
                .then(function (responses) {
                    console.log(responses)
                    that.setState({
                        response: {
                            success: responses.data.success,
                            message: responses.data.message,
                            min_cost: responses.data.cost,
                            matrix: responses.data.matrix
                        }
                    }, () => {
                        console.log(that.state)
                        that.setState(
                            {is_received: true})
                    })
                })
                .catch(function (error) {
                    console.log(error)
                })
        }
    }

    inputboxGenerate() {
        return <table>
            <tbody>
            <tr>
                <td>
                    产地/销地
                </td>
                {this.state.matrix[0].map((element, index) =>
                    index < this.state.sale_num &&
                    <td key={"col" + index}>
                        B{index + 1}
                    </td>)}
                <td>
                    产量
                </td>
            </tr>
            {this.state.matrix.map((line, index) =>
                index < this.state.produce_num &&
                <tr key={"row" + index}>
                    <td>A{index + 1}</td>
                    {line.map((e, index2) =>
                        index2 < this.state.sale_num &&
                        <td key={"e" + index + index2}>
                            <input type="number" name={index + " " + index2}
                                   onChange={this.handleMatrixChange}
                                   value={this.state.matrix[index][index2]}/>
                        </td>)
                    }
                    <td>
                        <input type="number" name={index + " " + (this.state.sale_num)}
                               onChange={this.handleMatrixChange}
                               value={this.state.matrix[index][this.state.sale_num]}/>
                    </td>
                </tr>)}
            <tr>
                <td>
                    销量
                </td>
                {this.state.matrix[0].map((_, index) =>
                    index < this.state.sale_num &&
                    <td key={"sale" + index}>
                        <input type="number" name={(this.state.produce_num) + " " + index}
                               onChange={this.handleMatrixChange}
                               value={this.state.matrix[this.state.produce_num][index]}/>
                    </td>)}
            </tr>
            </tbody>
        </table>
    }


    resultBoxGenerator() {
        return <div>
            <span>message: {this.state.response.message}</span>
            <br/>
            {this.state.response.success &&
            <div>
                <span>最小成本为： {this.state.response.min_cost}</span>
                <br/>
                <span>迭代后的x矩阵：</span>
                <div>
                    <table>
                        <tbody>
                        <tr>
                            <td>
                                产地/销地
                            </td>
                            {this.state.response.matrix[0].map((element, index) =>
                                <td key={"matrix_col" + index}>
                                    B{index + 1}
                                </td>)}
                        </tr>
                        {this.state.response.matrix.map((line, index) =>
                            <tr key={"matrix_row" + index}>
                                <td>A{index + 1}</td>
                                {line.map((e, index2) =>
                                    <td key={"matrix_e" + index + index2}>
                                        {e}
                                    </td>)
                                }
                            </tr>)}
                        </tbody>
                    </table>
                </div>
            </div>

            }
        </div>
    }

    render() {

        return (
            <div>
                <span>
                    请输入产地数量： <input type="number" name="produce_num" value={this.state.produce_num}
                                    onChange={this.handleNumberChange}/>
                </span>
                <br/>
                <span>
                    请输入销地数量： <input type="number" name="sale_num" value={this.state.sale_num}
                                    onChange={this.handleNumberChange}/>
                </span>
                <br/>
                {
                    this.state.show_input ?
                        <div>
                            {this.inputboxGenerate()}
                            {
                                this.state.is_received ? <div>{this.resultBoxGenerator()}</div> :
                                    <button type="submit" onClick={() => {
                                        this.upload()
                                    }}>提交
                                    </button>
                            }
                        </div> :
                        <div>
                            <button type="submit" onClick={() => {
                                this.handleNumberSubmit()
                            }}>提交
                            </button>
                        </div>

                }

            </div>

        );


    }
}

export default Transportation