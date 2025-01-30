# _plugins/alert_block_converter.rb

module Jekyll
    class AlertBlockConverter < Converter
      safe true
      priority :high
  
      # This converter applies to Markdown files
      def matches(ext)
        ext =~ /^\.md$/i
      end
  
      # Output will be HTML
      def output_ext(ext)
        ".html"
      end
  
      # Convert the content
      def convert(content)
        # Regular expression to match ::: type ... ::: blocks
        # This regex supports multiple lines and multiple blocks
        content = content.gsub(/:::\s*(tip|warning|error|lemma|theorem)\s*\n(.*?)\n:::/m) do
          type = Regexp.last_match(1)
          inner_content = Regexp.last_match(2)
  
          # Convert the inner markdown content to HTML
          html_content = Kramdown::Document.new(inner_content, @config['kramdown']).to_html
  
          # Return the div with appropriate classes
          %Q(<div class="alert alert-#{type}">\n#{html_content}\n</div>)
        end
  
        # Convert the entire modified content to HTML
        Kramdown::Document.new(content, @config['kramdown']).to_html
      end
    end
  end
  