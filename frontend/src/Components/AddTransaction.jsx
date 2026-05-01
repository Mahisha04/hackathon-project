import { useState } from "react"
import axios from "axios"

export default function AddTransaction({ onAdded }) {
  const [form, setForm] = useState({ sender: "", receiver: "", amount: "" })
  const [status, setStatus] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async () => {
    if (!form.sender || !form.receiver || !form.amount) {
      setStatus({ type: "error", msg: "Please fill all fields." })
      return
    }
    setLoading(true)
    try {
      const res = await axios.post("http://localhost:8000/add", {
        sender: form.sender,
        receiver: form.receiver,
        amount: parseFloat(form.amount),
      })
      const isSuspicious = res.data.suspicious
      setStatus({
        type: isSuspicious ? "warning" : "success",
        msg: isSuspicious
          ? `⚠️ Block #${res.data.block_index} added — SUSPICIOUS amount flagged!`
          : `✅ Block #${res.data.block_index} added successfully!`,
      })
      setForm({ sender: "", receiver: "", amount: "" })
      onAdded()
    } catch {
      setStatus({ type: "error", msg: "Failed to connect to backend." })
    }
    setLoading(false)
  }

  return (
    <div className="bg-white rounded-2xl shadow p-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">Add Transaction</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="text-sm text-gray-500 block mb-1">Sender</label>
          <input
            name="sender"
            value={form.sender}
            onChange={handleChange}
            placeholder="e.g. Ministry of Health"
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>
        <div>
          <label className="text-sm text-gray-500 block mb-1">Receiver</label>
          <input
            name="receiver"
            value={form.receiver}
            onChange={handleChange}
            placeholder="e.g. City Hospital"
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>
        <div>
          <label className="text-sm text-gray-500 block mb-1">Amount ($)</label>
          <input
            name="amount"
            value={form.amount}
            onChange={handleChange}
            type="number"
            placeholder="e.g. 50000"
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </div>
      </div>
      <button
        onClick={handleSubmit}
        disabled={loading}
        className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Adding..." : "Add to Blockchain"}
      </button>
      {status && (
        <p className={`mt-3 text-sm font-medium ${
          status.type === "success" ? "text-green-600" :
          status.type === "warning" ? "text-orange-500" : "text-red-500"
        }`}>
          {status.msg}
        </p>
      )}
    </div>
  )
}