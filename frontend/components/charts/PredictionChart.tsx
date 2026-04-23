'use client'
import { Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import { Prediction } from '@/types'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

export default function PredictionChart({ data }: { data: Prediction[] }) {
  // Sorting by probability for high-to-low aesthetic in horizontal bar
  const sorted = [...data].sort((a, b) => b.probability - a.probability)

  const chartData = {
    labels: sorted.map((p) => p.class),
    datasets: [
      {
        data: sorted.map((p) => p.probability),
        backgroundColor: [
          '#BA6E8F', // Primary pick
          '#D391B0',
          '#9F6496',
          '#7B466A',
          '#5A324E',
        ],
        borderRadius: 12,
        borderWidth: 0,
        barThickness: 24,
      },
    ],
  }

  const options = {
    indexAxis: 'y' as const,
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: '#0C0420',
        titleColor: '#D391B0',
        bodyColor: '#FFFFFF',
        borderColor: '#BA6E8F',
        borderWidth: 1,
        padding: 12,
        cornerRadius: 12,
        callbacks: {
          label: (ctx: any) => ` ${ctx.parsed.x.toFixed(2)}% confidence`,
        },
      },
    },
    scales: {
      x: {
        grid: {
          display: true,
          color: 'rgba(255, 255, 255, 0.05)',
        },
        ticks: {
          color: '#7B466A',
          font: {
            size: 11,
            weight: 'bold' as const,
          },
          callback: (value: any) => `${value}%`,
        },
        max: 100,
        beginAtZero: true,
      },
      y: {
        grid: {
          display: false,
        },
        ticks: {
          color: '#FFFFFF',
          font: {
            size: 13,
            weight: 'bold' as const,
          },
        },

      },
    },
    animation: {
      duration: 2000,
      easing: 'easeOutQuart' as const,
    },
  }

  return (
    <div className="w-full h-full p-4 glass rounded-3xl">
      <Bar data={chartData} options={options} />
    </div>
  )
}