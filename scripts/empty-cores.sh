echo "Emptying cores: $@"

for core in "$@"; do
    curl "http://solr:8983/solr/$core/update?stream.body=<delete><query>*:*</query></delete>&commit=true"
done