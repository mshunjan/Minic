import * as d3 from 'd3'
import StackedBarChart from './StackedBarChart'
import { useEffect, useState, useRef} from 'react'

const Chart = ({data}) => { 
    const svg = useRef(null);

    const create_records = (data) => {
        let records = []
        let species = []
        let samples = Object.keys(data)
        samples.forEach((sample) => {
            let sample_keys = Object.keys(data[sample])
            sample_keys.forEach((k) => {
                species.push(k)
                records.push(
                    {
                        'sample': sample,
                        'species': k,
                        'abundance': data[sample][k]
                    }
                )
            })
        })
        species = species.filter(function (value, index, array) {
            return array.indexOf(value) === index;
        })
        return { 'records': records, 'species': species }
    }
    
    useEffect(() => {
        let records = create_records(data)
        if (Object.keys(records).length != 0) {
            let chart_records = records?.records
            let species = records?.species
            const chart = StackedBarChart(chart_records, {
                x: d => d.sample,
                y: d => d.abundance,
                z: d => d.species,
                yLabel: "↑ Relative Abundance (%)",
                zDomain: species,
                width: 1000,
                height: 1000,
                colors: d3.schemeSpectral[species.length],
            })
            if (svg.current) {
                svg.current.appendChild(chart)
            }
        }
    }, [data]);

    return (
        <div ref={svg} />
    )
}

export default Chart; 