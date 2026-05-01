import { useState } from "react"
import AddTransaction from "./components/AddTransaction"
import Dashboard from "./components/Dashboard"

export default function App() {
  const [refresh, setRefresh] = useState(0)

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-blue-700 text-white py-5 px-6 shadow">
        <h1 className="text-2xl font-bold">🔗 Blockchain Public Fund Tracker</h1>
        <p className="text-blue-200 text-sm mt-1">Transparent. Immutable. Trustworthy.</p>
      </header>
      <main className="max-w-4xl mx-auto p-6 space-y-8">
        <AddTransaction onAdded={() => setRefresh(r => r + 1)} />
        <Dashboard key={refresh} />
      </main>
    </div>
  )
}