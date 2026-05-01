import { useEffect, useState } from "react"
import axios from "axios"

export default function Dashboard() {
  const [chain, setChain] = useState([])
  const [valid, setValid] = useState(true)

  useEffect(() => {
    axios.get("http://localhost:8000/chain").then((res) => {
      setChain(res.data.chain)
      setValid(res.data.valid)
    })
  }, [])

  const realBlocks = chain.filter((b) => b.index !== 0)

  return (
    <div className="bg-white rounded-2xl shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-800">Transaction Ledger</h2>
        <span className={`text-xs px-3 py-1 rounded-full font-medium ${
          valid ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
        }`}>
          {valid ? "✅ Chain Valid" : "❌ Chain Tampered!"}
        </span>
      </div>

      {realBlocks.length === 0 ? (
        <p className="text-gray-400 text-sm">No transactions yet. Add one above!</p>
      ) : (
        <div className="space-y-3">
          {realBlocks.map((block) => (
            <div
              key={block.index}
              className={`border rounded-xl p-4 ${
                block.data.suspicious
                  ? "border-orange-300 bg-orange-50"
                  : "border-gray-100 bg-gray-50"
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-semibold text-gray-700">
                  Block #{block.index}
                </span>
                {block.data.suspicious && (
                  <span className="text-xs bg-orange-200 text-orange-800 px-2 py-0.5 rounded-full font-medium">
                    ⚠️ Suspicious
                  </span>
                )}
              </div>
              <div className="grid grid-cols-3 gap-2 text-sm mb-2">
                <div>
                  <p className="text-gray-400 text-xs">Sender</p>
                  <p className="text-gray-800 font-medium">{block.data.sender}</p>
                </div>
                <div>
                  <p className="text-gray-400 text-xs">Receiver</p>
                  <p className="text-gray-800 font-medium">{block.data.receiver}</p>
                </div>
                <div>
                  <p className="text-gray-400 text-xs">Amount</p>
                  <p className="text-gray-800 font-medium">
                    ${Number(block.data.amount).toLocaleString()}
                  </p>
                </div>
              </div>
              <p className="text-xs text-gray-400 font-mono truncate">
                Hash: {block.hash}
              </p>
              <p className="text-xs text-gray-300 font-mono truncate">
                Prev: {block.previous_hash}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}