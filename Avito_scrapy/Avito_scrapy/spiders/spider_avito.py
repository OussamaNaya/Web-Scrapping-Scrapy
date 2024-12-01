import scrapy


class SpiderAvitoSpider(scrapy.Spider):
    name = "spider_avito"
    allowed_domains = ["www.avito.ma"]
    start_urls = ["https://www.avito.ma/fr/maroc/voitures_d_occasion-%C3%A0_vendre"]

    def parse(self, response):
        list_voiture = response.css('a.sc-1jge648-0.eTbzNs')

        if len(list_voiture) == 0:
            return None

        for voiture in list_voiture:
            href = voiture.attrib['href']
            temp_pub = voiture.css('p.sc-1x0vz2r-0.iFQpLP::text').get()
            image = voiture.css('img.sc-bsm2tm-3.krcAcS').attrib['src']
            name = voiture.css('p.sc-1x0vz2r-0.czqClV::text').get()
            equipement = voiture.css('span.sc-1s278lr-0.fkuRXf *::text').getall()
            if equipement:
                annee = equipement[0]
                boite_vettesse = equipement[2]
                moteur = equipement[4]
            else:
                annee = ''
                boite_vettesse = ''
                moteur = ''
            
            prix = voiture.css('p.sc-1x0vz2r-0.eCXWei.sc-b57yxx-3.IneBF::text').get()


            yield{
                'href': href,
                'temp_pub': temp_pub,
                'image' : image,
                'name': name,
                'annee': annee,
                'boite_vettesse': boite_vettesse,
                'moteur' : moteur,
                'prix' : prix,
            }

        fouter = response.css('div.sc-2y0ggl-0.hInuCx')
        next_page = fouter.css('a.sc-1cf7u6r-0.gRyZxr.sc-2y0ggl-1.yRCEb')[-1].attrib['href']

        num_page = int(next_page.split('?')[-1].split('=')[-1])
        if num_page > 50:
            return None
        
        # Appele recurcive
        yield response.follow(next_page, callback=self.parse)
