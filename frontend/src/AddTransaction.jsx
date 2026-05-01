import { useState } from "react"
import axios from "axios"
import { motion } from "framer-motion"
import toast from "react-hot-toast"

export default function AddTransaction({ onAdded }) {
  const [form, setForm] = useState({
    sender: "",
    receiver: "",
    amount: ""
  })

  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async () => {
    if (!form.sender || !form.receiver || !form.amount) {
      toast.error("Fill all fields ⚠️")
      return
    }

    setLoading(true)
    toast.loading("⛏ Mining block...")

    try {
      const res = await axios.post("http://localhost:8000/add", {
        sender: form.sender,
        receiver: form.receiver,
        amount: parseFloat(form.amount),
      })

      toast.dismiss()

      if (res.data.suspicious) {
        toast.error("⚠️ Suspicious transaction!")
      } else {
        toast.success(`🔥 Block #${res.data.block_index} mined!`)
      }

      setForm({ sender: "", receiver: "", amount: "" })
      onAdded()
    } catch {
      toast.dismiss()
      toast.error("Backend error ❌")
    }

    setLoading(false)
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass p-6"
    >
      <h2 className="text-xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
        Add Transaction
      </h2>

      <div className="grid md:grid-cols-3 gap-4">
        <input
          name="sender"
          value={form.sender}
          onChange={handleChange}
          placeholder="Sender"
          className="input"
        />

        <input
          name="receiver"
          value={form.receiver}
          onChange={handleChange}
          placeholder="Receiver"
          className="input"
        />

        <input
          name="amount"
          type="number"
          value={form.amount}
          onChange={handleChange}
          placeholder="Amount"
          className="input"
        />
      </div>

      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={handleSubmit}
        disabled={loading}
        className="mt-5 bg-gradient-to-r from-blue-500 to-indigo-600 px-6 py-3 rounded-xl font-semibold shadow-lg hover:shadow-blue-500/40 transition"
      >
        {loading ? "Mining..." : "Add to Blockchain"}
      </motion.button>
    </motion.div>
  )
}