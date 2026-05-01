import { useEffect, useState } from "react"
import axios from "axios"
import { motion } from "framer-motion"
import Charts from "./Charts"
import Timeline from "./Timeline"
import ThreeD from "./ThreeD"

export default function Dashboard() {
  const [chain, setChain] = useState([])
  const [valid, setValid] = useState(true)

  const [search, setSearch] = useState("")
  const [filter, setFilter] = useState("all")

  useEffect(() => {
    axios.get("http://localhost:8000/chain").then((res) => {
      setChain(res.data.chain)
      setValid(res.data.valid)
    })
  }, [])

  const realBlocks = chain.filter((b) => b.index !== 0)

  const total = realBlocks.reduce((sum, b) => sum + b.data.amount, 0)
  const suspicious = realBlocks.filter((b) => b.data.suspicious).length

  // 🔍 FILTER LOGIC
  const filtered = realBlocks.filter((b) => {
    const matchSearch =
      b.data.sender.toLowerCase().includes(search.toLowerCase()) ||
      b.data.receiver.toLowerCase().includes(search.toLowerCase())

    const matchFilter =
      filter === "all" ||
      (filter === "suspicious" && b.data.suspicious) ||
      (filter === "safe" && !b.data.suspicious)

    return matchSearch && matchFilter
  })

  return (
    <div className="space-y-6">

      {/* 🔥 STATS */}
      <div className="grid md:grid-cols-3 gap-4">
        <div className="glass p-4 text-center">
          <p>Total Transactions</p>
          <h2 className="text-2xl font-bold">{realBlocks.length}</h2>
        </div>

        <div className="glass p-4 text-center">
          <p>Total Amount</p>
          <h2 className="text-2xl font-bold">
            ${total.toLocaleString()}
          </h2>
        </div>

        <div className="glass p-4 text-center">
          <p>Suspicious</p>
          <h2 className="text-2xl font-bold text-orange-400">
            {suspicious}
          </h2>
        </div>
      </div>

      {/* 📊 CHARTS */}
      <Charts data={realBlocks} />

      {/* 🔗 TIMELINE */}
      <Timeline blocks={realBlocks} />

      {/* 🌌 3D VIEW */}
      <ThreeD blocks={realBlocks} />

      {/* 📜 LEDGER */}
      <div className="glass p-6">

        {/* HEADER */}
        <div className="flex justify-between mb-4">
          <h2 className="text-lg font-bold">
            Transaction Ledger
          </h2>

          <span className={valid ? "text-green-400" : "text-red-400"}>
            {valid ? "✅ Valid Chain" : "❌ Tampered"}
          </span>
        </div>

        {/* 🔍 SEARCH + FILTER */}
        <div className="flex gap-3 mb-4">
          <input
            placeholder="Search..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input w-1/2"
          />

          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="input"
          >
            <option value="all">All</option>
            <option value="safe">Safe</option>
            <option value="suspicious">Suspicious</option>
          </select>
        </div>

        {/* LIST */}
        <div className="space-y-3">
          {filtered.map((block, i) => {
            const risk = block.data.suspicious ? "High" : "Low"

            return (
              <motion.div
                key={block.index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className={`p-4 rounded-xl border transition ${
                  block.data.suspicious
                    ? "border-orange-400 bg-orange-500/10 hover:shadow-orange-500/30"
                    : "border-white/20 bg-white/5 hover:shadow-blue-500/30"
                }`}
              >
                <div className="flex justify-between mb-2">
                  <p className="font-semibold">
                    Block #{block.index}
                  </p>

                  <span className="text-xs px-2 py-1 rounded bg-white/10">
                    Risk: {risk}
                  </span>
                </div>

                <div className="grid grid-cols-3 text-sm">
                  <p>{block.data.sender}</p>
                  <p>{block.data.receiver}</p>
                  <p>${block.data.amount}</p>
                </div>

                <p className="text-xs opacity-60 mt-2 truncate">
                  Hash: {block.hash}
                </p>
              </motion.div>
            )
          })}
        </div>

      </div>

    </div>
  )
}