import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip } from "chart.js";
ChartJS.register(ArcElement, Tooltip);

export default function SeverityPie() {
  return <Pie data={{
    labels:["High","Medium","Low"],
    datasets:[{ data:[40,30,30], backgroundColor:["#ef4444","#facc15","#22c55e"] }]
  }} />;
}