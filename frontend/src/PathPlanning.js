import React from "react";
import axios from "axios";

class PathPlaningPage extends React.Component {
    render() {
        return <Canvas width={1000} height={1000} size={20}/>
    }
}

class Canvas extends React.Component {
    constructor(props) {
        //props: 栅格地图长宽
        super(props);
        this.state = {
            src: Array(),
            des: Array(),
            blocks: Array(),
            button_status: "src", //src des blocks
            path: Array(),
            close_list: Array()
        }

        this.handleSubmit = this.handleSubmit.bind(this)

    }

    //绘制基础图样
    draw_gird(ctx, grid_size) {
        var width = ctx.canvas.width;
        var height = ctx.canvas.height;

        var xl_num = Math.floor(width / grid_size)
        for (let i = 0; i < xl_num; i++) {
            ctx.beginPath()
            ctx.moveTo(0, grid_size * i - 0.5)
            ctx.lineTo(height, grid_size * i - 0.5)
            ctx.strokeStyle = "#ccc";
            ctx.stroke();
        }


        var yl_num = Math.floor(height / grid_size)
        for (let i = 0; i < yl_num; i++) {
            ctx.beginPath()
            ctx.moveTo(grid_size * i, 0)
            ctx.lineTo(grid_size * i, width)
            ctx.strokeStyle = "#ccc";
            ctx.stroke();
        }
    }

    //点击坐标转换为坐标位置
    transferToPoint(e, grid_size) {
        return {
            x: Math.floor(e.layerX / grid_size),
            y: Math.floor(e.layerY / grid_size)
        }
    }

    //xy坐标位置  不是像素位置 color自选
    changeGridColor(ctx, pose, color) {
        ctx.fillStyle = color
        let size = this.props.size
        ctx.fillRect(pose[0] * size, pose[1] * size, size, size)
    }

    restoreGrid(ctx, x, y) {
        x *= this.props.size
        y *= this.props.size
        ctx.clearRect(x, y, this.props.size, this.props.size);
        ctx.beginPath()
        ctx.moveTo(x, y)
        ctx.lineTo(x, y + this.props.size - 0.5)
        ctx.lineTo(x + this.props.size, y + this.props.size - 0.5)
        ctx.lineTo(x + this.props.size, y)
        ctx.strokeStyle = "#ccc"
        ctx.stroke();
    }

    createGridListener(grid, ctx) {
        let that = this
        grid.addEventListener('click', function (e) {
            // console.log(that.transferToPoint(e, that.props.size))
            //layerX layerY 表示点击的相对位置
            let point = that.transferToPoint(e, that.props.size)

            // that.changeGridColor(ctx, [point.x, point.y], "orange")

            switch (that.state.status) {
                case "src":
                    if (that.state.src.length === 0) {
                        that.setState({src: [point.x, point.y]}, () => {
                            that.changeGridColor(ctx, that.state.src, "orange")
                        })
                    } else {
                        let tmp = that.state.src;
                        that.setState({src: [point.x, point.y]}, () => {
                            that.restoreGrid(ctx, tmp[0], tmp[1])
                            that.changeGridColor(ctx, that.state.src, "orange")
                        })
                    }

                    break
                case "des":
                    if (that.state.des.length === 0) {
                        that.setState({des: [point.x, point.y]}, () => {
                            that.changeGridColor(ctx, that.state.des, "blue")
                        })
                    } else {
                        let tmp = that.state.des;
                        that.setState({des: [point.x, point.y]}, () => {
                            that.restoreGrid(ctx, tmp[0], tmp[1])
                            that.changeGridColor(ctx, that.state.des, "blue")
                        })
                    }
                    break
                case "blocks":
                    that.setState({blocks: [...that.state.blocks, [point.x, point.y]]}, () => {
                        that.changeGridColor(ctx, [point.x, point.y], "black")
                    })
                    break
                default:
                    break
            }
        })
    }

    componentDidMount() {
        let grid = document.querySelector("#gridCanvas")
        let ctx = grid.getContext('2d');
        this.draw_gird(ctx, this.props.size)
        this.createGridListener(grid, ctx)
    }

    handleSubmit() {
        let that = this
        axios.post('http://127.0.0.1:5000/astar', {
            'size': Math.floor(this.props.width / this.props.size),
            'src': this.state.src,
            'des': this.state.des,
            'blocks': this.state.blocks
        })
            .then(function (responses) {

                that.setState({
                        path: responses.data.path,
                        close_list: responses.data.close_list
                    },
                    () => {
                        console.log(that.state)
                        let time_interval = 1
                        for (let c in that.state.close_list) {
                            let ctx = document.querySelector("#gridCanvas").getContext("2d")
                            setTimeout(() => that.changeGridColor(ctx, that.state.close_list[c], "green"), time_interval * 20)
                            time_interval++
                        }
                        for (let c in that.state.path) {
                            let ctx = document.querySelector("#gridCanvas").getContext("2d")
                            setTimeout(() => that.changeGridColor(ctx, that.state.path[c], "red"), time_interval * 20)
                            time_interval++
                        }
                    })
            })
            .catch(function (error) {
                console.log(error)
            })
    }

    render() {
        let grid_canvas = <canvas id="gridCanvas" width={this.props.width} height={this.props.height}></canvas>
        let that = this
        let ctx;
        /*        window.onload = function () {

                }*/

        return (
            <div>
                {grid_canvas}
                <div>
                    {/*一次确保只有一个标志位打开*/}
                    <button type="submit"
                            onClick={() => this.setState({status: "src"})}>设置起点
                    </button>
                    <button type="submit"
                            onClick={() => this.setState({status: "des"})}>设置终点
                    </button>
                    <button type="submit"
                            onClick={() => this.setState({status: "blocks"})}>设置障碍物
                    </button>
                    <button type="submit"
                            onClick={() => window.location.reload()}>清除
                    </button>
                    <button type="submit" onClick={this.handleSubmit}>提交</button>

                </div>
            </div>


        )
    }
}

export default PathPlaningPage;