import { Line } from "react-chartjs-2";
import { Chart as ChartJS, LineElement, CategoryScale, LinearScale, PointElement } from "chart.js";
ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

export default function AccidentTrend() {
  return <Line data={{
    labels:["Jan","Feb","Mar","Apr","May","Jun"],
    datasets:[
      { label:"High", data:[12,15,14,18,20,22], borderColor:"#ef4444" },
      { label:"Medium", data:[8,10,9,11,13,15], borderColor:"#facc15" },
      { label:"Low", data:[5,6,7,6,8,9], borderColor:"#22c55e" }
    ]
  }} />;
}