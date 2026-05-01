import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell
} from "recharts"

export default function Charts({ data }) {
  const chartData = data.map((b) => ({
    name: `B${b.index}`,
    amount: b.data.amount
  }))

  const pieData = [
    { name: "Safe", value: data.filter(b => !b.data.suspicious).length },
    { name: "Suspicious", value: data.filter(b => b.data.suspicious).length }
  ]

  const COLORS = ["#22c55e", "#f97316"]

  return (
    <div className="grid md:grid-cols-2 gap-4">

      {/* BAR */}
      <div className="glass p-6">
        <h2 className="font-bold mb-3">Transaction Volume</h2>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={chartData}>
            <XAxis dataKey="name" stroke="#ccc" />
            <YAxis stroke="#ccc" />
            <Tooltip />
            <Bar dataKey="amount" fill="#3b82f6" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* PIE */}
      <div className="glass p-6">
        <h2 className="font-bold mb-3">Risk Distribution</h2>
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie data={pieData} dataKey="value" outerRadius={80}>
              {pieData.map((entry, index) => (
                <Cell key={index} fill={COLORS[index]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>

    </div>
  )
}