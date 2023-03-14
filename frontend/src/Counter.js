import React from "react";
import axios from "axios";

class CounterPage extends React.Component {
    render() {
        return <InputBox/>
    }
}

class InputBox extends React.Component {
    constructor() {
        super();
        this.state = {
            col_number: 2,
            row_number: 2,
            show_input: false,
            matrix: Array(),
            is_received: false,
            responce: {
                result: [],
                message: ""
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
        // let tmp = Array();
        // for (let i = 0; i < this.state.row_number; i++) {
        //     let line_tmp = Array();
        //     for (let j = 0; j < this.state.col_number; j++) {
        //         line_tmp = [...line_tmp, ""]
        //     }
        //     tmp[i] = line_tmp
        // }
        let tmp = [[7, 4], [3, 6]]
        this.setState({
            matrix: tmp
        }, () => {
            this.setState({show_input: true})
        })
    }

    handleMatrixChange(event) {
        // if (event.target.value <= 0) {
        //     alert("请输入非负数")
        //     return
        // }
        let index1 = event.target.name.split(" ")[0]
        let index2 = event.target.name.split(" ")[1]
        let tmp = this.state.matrix
        tmp[index1][index2] = event.target.value
        this.setState({matrix: tmp}, () => console.log(this.state))
    }

    upload(event) {
        let that = this
        if (this.state.matrix.filter(
            (line) => {
                return line.filter((e) => {
                    return e === ''
                }).length > 0
            }).length > 0
        ) {
            alert("not finish")
            return null;
        } else {
            console.log("发送请求")
            axios.post('http://127.0.0.1:5000/counter', {
                "matrix": this.state.matrix,
                "method": event.target.name
            })
                .then(function (responses) {
                    console.log(responses)
                    that.setState({
                        responce: {
                            result: responses.data.result,
                            message: responses.data.message
                        }
                    }, () => {
                        that.setState({is_received: true})
                        console.log(that.state)
                    })
                })
                .catch(function (error) {
                    console.log(error)
                })
        }
    }

    generateInputBox() {
        return <table>
            <tbody>
            <tr>
                <td/>
                {this.state.matrix[0].map((e, index) => <td key={"counter_mat_line_t" + index}>
                    B{index}
                </td>)}
            </tr>
            {this.state.matrix.map((line, index) =>
                <tr key={"counter_mat_line" + index}>
                    <td>A{index}</td>
                    {line.map((e, index2) => <td key={"counter_mat" + index + index2}>
                        <input type="number"
                               name={index + " " + index2}
                               onChange={this.handleMatrixChange}
                               value={this.state.matrix[index][index2]}/>
                    </td>)}
                </tr>)}
            </tbody>
        </table>
    }

    render() {
        return (
            <div>
                <span>
                    请输入行策略数： <input type="number" name="row_number" value={this.state.row_number}
                                    onChange={this.handleNumberChange}/>
                </span>
                <br/>
                <span>
                    请输入列策略数： <input type="number" name="col_number" value={this.state.col_number}
                                    onChange={this.handleNumberChange}/>
                </span>
                <br/>
                {!this.state.show_input ?
                    <button type="submit" onClick={() => {
                        this.handleNumberSubmit()
                    }}>提交
                    </button> :
                    <div>
                        {this.generateInputBox()}
                        <button type="submit" onClick={this.upload} name={"pure"}>pure提交</button>
                        <button type="submit" onClick={this.upload} name={"mixed"}>mixed提交</button>
                    </div>}
            </div>
        );
    }


}

export default CounterPage;
