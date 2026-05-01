import { useState } from "react"
import AddTransaction from "./components/AddTransaction"
import Dashboard from "./components/Dashboard"
import { Toaster } from "react-hot-toast"

export default function App() {
  const [refresh, setRefresh] = useState(0)

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-indigo-900 to-blue-900 text-white">
      
      <Toaster position="top-right" />

      <header className="p-6 border-b border-white/20 backdrop-blur-md bg-white/10">
        <h1 className="text-3xl font-bold">
          🔗 Blockchain Fund Tracker
        </h1>
        <p className="text-gray-300 text-sm">
          Transparent • Immutable • Intelligent
        </p>
      </header>

      <main className="max-w-5xl mx-auto p-6 space-y-6">
        <AddTransaction onAdded={() => setRefresh(r => r + 1)} />
        <Dashboard key={refresh} />
      </main>

    </div>
  )
}