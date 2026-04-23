'use client'

import { Line } from 'react-chartjs-2'
import { useHistory } from '@/hooks/useHistory'
import { DateTime } from 'luxon'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

export default function HistoryChart() {
  const { history } = useHistory()

  // Process history data for the last 7 entries to show trends
  // We reverse it to show chronologically (oldest to newest)
  const recentHistory = [...history].slice(0, 10).reverse()
  
  const labels = recentHistory.map(item => 
    DateTime.fromISO(item.timestamp).toFormat('MMM dd, HH:mm')
  )
  
  const confidenceData = recentHistory.map(item => item.confidence)

  const data = {
    labels: labels.length > 0 ? labels : ['No Data'],
    datasets: [
      {
        label: 'Model Confidence %',
        data: confidenceData.length > 0 ? confidenceData : [0],
        borderColor: '#BA6E8F',
        backgroundColor: 'rgba(186, 110, 143, 0.1)',
        borderWidth: 3,
        pointBackgroundColor: '#BA6E8F',
        pointBorderColor: '#FFFFFF',
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 8,
        tension: 0.4,
        fill: true,
      }
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
        backgroundColor: '#0C0420',
        padding: 12,
        cornerRadius: 12,
        titleFont: { size: 14, weight: 'bold' as const },
        bodyFont: { size: 13 },
        callbacks: {
          label: (context: any) => ` Confidence: ${context.parsed.y.toFixed(1)}%`
        }
      },
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { 
          color: '#7B466A', 
          font: { weight: 'bold' as const, size: 10 },
          maxRotation: 45,
          minRotation: 45
        },
      },
      y: {
        grid: { color: 'rgba(255, 255, 255, 0.05)' },
        ticks: { 
          color: '#7B466A',
          callback: (value: any) => `${value}%`
        },
        beginAtZero: true,
        max: 100
      },
    },
    animation: {
      duration: 2000,
      easing: 'easeOutQuart' as const,
    },
  }

  return (
    <div className="w-full h-full glass p-4 md:p-8 rounded-[2.5rem] border-white/5">
      {history.length === 0 ? (
        <div className="flex items-center justify-center h-full text-gray-500 font-bold italic">
          Insufficient data for visualization
        </div>
      ) : (
        <Line data={data} options={options} />
      )}
    </div>
  )
}
