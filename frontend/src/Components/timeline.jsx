import { motion } from "framer-motion"

export default function Timeline({ blocks }) {
  return (
    <div className="glass p-6 overflow-x-auto">
      <h2 className="text-lg font-bold mb-4">Blockchain Timeline</h2>

      <div className="flex gap-6">
        {blocks.map((block, i) => (
          <motion.div
            key={block.index}
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.2 }}
            className="min-w-[180px] bg-white/10 p-4 rounded-xl border border-white/20"
          >
            <p className="font-semibold mb-2">Block #{block.index}</p>
            <p className="text-sm">{block.data.sender}</p>
            <p className="text-sm">→ {block.data.receiver}</p>
            <p className="text-sm font-bold mt-1">${block.data.amount}</p>
          </motion.div>
        ))}
      </div>
    </div>
  )
}