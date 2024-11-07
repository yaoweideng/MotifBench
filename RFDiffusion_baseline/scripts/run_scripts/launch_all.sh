gpu_count=8  # Replace with the actual number of GPUs available
i=0
ls run* | while read l; do
    # Find an available GPU by checking for processes using each GPU
    while true; do
        gpu_id=$((i % gpu_count))
        
        # Check if there are any processes running on this GPU
        if ! nvidia-smi -i $gpu_id | grep -q "No running processes found"; then
            # If GPU is busy, increment index to check the next GPU
            i=$((i + 1))
            sleep 1  # Wait for a second before rechecking
            continue
        fi

        # GPU is free; assign job to this GPU and increment index
        echo "Running $l on GPU $gpu_id"
        CUDA_VISIBLE_DEVICES=$gpu_id bash "$l" &
        i=$((i + 1))
        sleep 1  # Add a small delay before starting the next job
        break
    done
done
