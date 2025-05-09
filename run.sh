#!/bin/bash

start_time=$(date '+%s')

source test/bin/activate

full_start_time=$(date '+%s')

echo "running 8b use-full-precision.py" > log
python3 main.py 8 full 1> result/full-stdout 2> result/full-stderr
echo "done for running 8b use-full-precision.py" >> log

full_end_time=$(date '+%s')

full_diff=$((full_end_time - full_start_time))
full_day=$((full_diff / (3600 * 24)))
full_hour=$((full_diff / 3600 % 24))
full_minute=$((full_diff / 60 % 60))
full_second=$((full_diff % 60))

echo "Total time: $full_day days $full_hour h $full_minute m $full_second s" >> log

echo "removing ~/.cache/huggingface dir" >> log
rm -rf ~/.cache/huggingface
echo "done for removing" >> log


echo "ollama serve" >> log
ollama serve &

sleep 60

echo "ollama pull deepseek-r1:70b" >> log
ollama pull deepseek-r1:70b

quantized_start_time=$(date '+%s')

echo "running use-quantized.py" >> log
python3 main.py 70 quantized 1> result/quantized-stdout 2> result/quantized-stderr
echo "done for running use-quantized.py" >> log

quantized_end_time=$(date '+%s')

quantized_diff=$((quantized_end_time - quantized_start_time))
quantized_day=$((quantized_diff / (3600 * 24)))
quantized_hour=$((quantized_diff / 3600 % 24))
quantized_minute=$((quantized_diff / 60 % 60))
quantized_second=$((quantized_diff % 60))

echo "Total time: $quantized_day days $quantized_hour h $quantized_minute m $quantized_second s" >> log

echo "removing deepseek r1 distill llama 70b" >> log
ollama rm deepseek-r1:8b

end_time=$(date '+%s')

diff=$((end_time - start_time))
day=$((diff / (3600 * 24)))
hour=$((diff / 3600 % 24))
minute=$((diff / 60 % 60))
second=$((diff % 60))

echo "Total time: $day days $hour h $minute m $second s" >> log

deactivate
