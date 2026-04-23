'use client'
import { Doughnut } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

export default function ConfidenceGauge({ confidence }: { confidence: number }) {
  const chartData = {
    labels: ['Confidence', 'Remaining'],
    datasets: [
      {
        data: [confidence, 100 - confidence],
        backgroundColor: [
          '#BA6E8F', // Accent
          'rgba(255, 255, 255, 0.05)', // Background track
        ],
        hoverBackgroundColor: ['#D391B0', 'rgba(255, 255, 255, 0.1)'],
        borderWidth: 0,
        borderRadius: 20,
        spacing: 5,
        cutout: '80%',
      },
    ],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        enabled: false,
      },
    },
    animation: {
      duration: 1500,
      easing: 'easeOutBack' as const,
    },
  }

  return (
    <div className="relative w-full h-full flex items-center justify-center">
      <Doughnut data={chartData} options={options} />
      <div className="absolute flex flex-col items-center justify-center text-center">
        <span className="text-4xl font-black text-white">{confidence.toFixed(1)}%</span>
        <span className="text-xs font-bold text-brand-secondary tracking-widest uppercase mt-1">
          Confidence
        </span>
      </div>
    </div>
  )
}
