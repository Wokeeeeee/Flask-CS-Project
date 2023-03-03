import React from "react";
import axios from "axios";
import dagreD3 from "dagre-d3";
import * as d3 from "d3";


class MaxStreamPage extends React.Component {
    render() {
        return <InputBox/>
    }
}

class InputBox extends React.Component {
    constructor() {
        super();
        this.state = {
            node_number: 6,
            edge_number: 8,
            show_input: false,
            edges: Array(),
            des: 5,
            src: 0,//测试用例之后全部置为""空字符串
            is_received: false,
            max_flow: 0,
            tuple: Array()
        }

        this.handleNumberChange = this.handleNumberChange.bind(this)
        this.handleNumberSubmit = this.handleNumberSubmit.bind(this)
        this.handleEdgeChange = this.handleEdgeChange.bind(this)
        this.upload = this.upload.bind(this)
    }

    handleNumberChange(event) {
        this.setState(
            {
                [event.target.name]: event.target.value
            }, () => console.log(this.state))
    }

    handleNumberSubmit() {
        // let tmp = this.state.edges
        // for (let i = 0; i < this.state.edge_number; i++) {
        //     tmp[i] = ["", "", ""]
        // }
        let tmp = [
            [0, 1, 3],
            [0, 2, 2],
            [1, 2, 1],
            [1, 3, 3],
            [1, 4, 4],
            [2, 4, 2],
            [3, 5, 2],
            [4, 5, 3]
        ]
        this.setState({
            edges: tmp
        }, () => {
            this.setState({show_input: true})
        })
    }

    handleEdgeChange(event) {
        if (event.target.value >= this.state.node_number) {
            alert("该数字超出节点数，请输入0-" + (this.state.node_number - 1) + "之间的数字")
            return
        }
        let index1 = event.target.name.split(" ")[0]
        let index2 = event.target.name.split(" ")[1]
        let tmp = this.state.edges
        tmp[index1][index2] = event.target.value
        this.setState({edges: tmp}, () => console.log(this.state))
    }

    upload() {
        let that = this
        if (this.state.edges.filter(
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
            axios.post('http://127.0.0.1:5000/maxflow', {
                'src': this.state.src,
                'des': this.state.des,
                'node_number': this.state.node_number,
                'edges': this.state.edges
            })
                .then(function (responses) {
                    console.log(responses)
                    that.setState({
                        tuple: responses.data.tuple,
                        result: responses.data.result
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

    render() {
        let edges_input =
            this.state.edges.map(
                (e, index) =>
                    <div key={"flow_input" + index}>
                        <span>src: <input type="number" name={index + " " + 0} onChange={this.handleEdgeChange}
                                          value={this.state.edges[index][0]}/></span>
                        <span>des: <input type="number" name={index + " " + 1} onChange={this.handleEdgeChange}
                                          value={this.state.edges[index][1]}/></span>
                        <span>capability: <input type="number" name={index + " " + 2} onChange={this.handleEdgeChange}
                                                 value={this.state.edges[index][2]}/></span>
                    </div>)


        return (
            <div>
                <span>
                    请输入节点数： <input type="number" name="node_number" value={this.state.node_number}
                                   onChange={this.handleNumberChange}/>
                </span>
                <br/>
                <span>
                    请输入有向边数： <input type="number" name="edge_number" value={this.state.edge_number}
                                    onChange={this.handleNumberChange}/>
                </span>
                <br/>
                {!this.state.show_input ?
                    <button type="submit" onClick={() => {
                        this.handleNumberSubmit()
                    }}>提交
                    </button> :
                    <div>
                        <span>
                            请输入起点： <input type="number" name="src" value={this.state.src}
                                          onChange={this.handleNumberChange}/>
                            请输入终点： <input type="number" name="des" value={this.state.des}
                                          onChange={this.handleNumberChange}/>
                        </span>
                        {edges_input}
                        <button type="submit" onClick={this.upload}>提交</button>
                    </div>}
                {
                    this.state.is_received === true &&
                    <div>
                        输入示意图：
                        <br/>
                        <div>
                            <VAG name="VAG1" size={this.state.node_number} tuple={this.state.edges}/>
                        </div>
                        {this.state.result === 0 ?
                            <div>
                                最大流结果为0，起点和终点不连通
                            </div> :
                            <div>
                                最大流结果为{this.state.result},输出示意图为：
                                <br/>
                                <VAG name="VAG2" size={this.state.node_number} tuple={this.state.tuple}/>
                            </div>}
                    </div>
                }
            </div>
        );
    }


}


class VAG extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            size: props.size,
            tuple: props.tuple
        }


    }

    generateDataset() {
        let nodes = Array(), edges = Array()
        for (let i = 0; i < this.state.size; i++) {
            nodes = [...nodes, {
                id: i, label: i.toString(), shape: "diamond"
            }]


        }
        for (let i in this.state.tuple) {
            let line = this.state.tuple[i]
            edges = [...edges,
                {
                    source: line[0], target: line[1], label: line[2]
                }]
        }
        return {
            nodes: nodes,
            edges: edges
        }
    }

    componentDidMount() {
        let dataset = this.generateDataset()
        /*let dataset = {
            nodes: [
                {id: 0, label: "流动人员", shape: "rect"},
                {id: 1, label: "安全筛查", shape: "rect"},
                {id: 2, label: "热像仪人体测温筛查", shape: "diamond"},
                {id: 3, label: "人工复测", shape: "diamond"},
                {id: 4, label: "快速通过", shape: "rect"},
                {id: 5, label: "紧急处理", shape: "rect"}
            ],
            edges: [
                {source: 0, target: 1, label: ""},
                {source: 1, target: 2, label: ""},
                {source: 2, target: 4, label: "正常"},
                {source: 2, target: 3, label: "不正常"},
                {source: 3, target: 5, label: "不正常"},
                {source: 3, target: 4, label: "正常"}
            ]
        }*/
        let g = new dagreD3.graphlib.Graph().setGraph({
            rankdir: 'LR', // 流程图从左到右显示，npm 默认‘TB’
            align: 'UL', // 设置节点对齐方式为下左
        })
        dataset.nodes.forEach((item, index) => {
            g.setNode(item.id, {label: item.label, shape: item.shape, style: "fill:#fff;stroke:#000"});
        });

        dataset.edges.forEach(item => {
            g.setEdge(item.source, item.target, {
                label: item.label,
                style: "fill:#fff;stroke:#afa;stroke-width:2px",
                labelStyle: "fill:#1890ff",
                arrowhead: "vee",
                arrowheadStyle: "fill:#f66"
            });
        });
        let render = new dagreD3.render();
// 选择 svg 并添加一个g元素作为绘图容器.
        let svgGroup = d3.select('#'+ this.props.name).append('g');
// 在绘图容器上运行渲染器生成流程图.
        render(svgGroup, g);
    }

    render() {

        return (
            <div className="App">
                <svg id={this.props.name} width="1000" height="1000"/>
            </div>
        );
    }
}


export default MaxStreamPage;
