import { Canvas } from "@react-three/fiber"
import { OrbitControls } from "@react-three/drei"

function Block({ position }) {
  return (
    <mesh position={position}>
      <boxGeometry args={[1,1,1]} />
      <meshStandardMaterial color="cyan" />
    </mesh>
  )
}

export default function ThreeD({ blocks }) {
  return (
    <div className="glass p-6 h-[300px]">
      <h2 className="font-bold mb-2">3D Blockchain</h2>

      <Canvas>
        <ambientLight />
        <pointLight position={[10,10,10]} />

        {blocks.map((b, i) => (
          <Block key={i} position={[i * 2, 0, 0]} />
        ))}

        <OrbitControls />
      </Canvas>
    </div>
  )
}