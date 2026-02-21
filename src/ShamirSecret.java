import java.io.FileReader;
import java.math.BigInteger;
import java.util.*;
import com.google.gson.*;

public class ShamirSecret {

    static class Share {
        int x;
        BigInteger y;

        Share(int x, BigInteger y) {
            this.x = x;
            this.y = y;
        }
    }

    public static void main(String[] args) throws Exception {

        String fileName = "test_case_1.json";

        JsonObject jsonObject = JsonParser.parseReader(new FileReader(fileName)).getAsJsonObject();
        JsonObject keys = jsonObject.getAsJsonObject("keys");

        int k = keys.get("k").getAsInt();

        List<Share> shares = new ArrayList<>();

        for (Map.Entry<String, JsonElement> entry : jsonObject.entrySet()) {

            if (entry.getKey().equals("keys")) continue;

            int x = Integer.parseInt(entry.getKey());
            JsonObject obj = entry.getValue().getAsJsonObject();

            int base = Integer.parseInt(obj.get("base").getAsString());
            String value = obj.get("value").getAsString();

            BigInteger y = new BigInteger(value, base);
            shares.add(new Share(x, y));
        }

        // Sort shares by x
        shares.sort(Comparator.comparingInt(s -> s.x));

        // Take first k shares
        List<Share> selected = shares.subList(0, k);

        BigInteger secret = lagrangeInterpolationAtZero(selected);

        System.out.println("Constant term (c) = " + secret);
        System.out.println("Digit length = " + secret.toString().length());
    }

    private static BigInteger lagrangeInterpolationAtZero(List<Share> shares) {

        BigInteger result = BigInteger.ZERO;

        for (int i = 0; i < shares.size(); i++) {

            BigInteger numerator = BigInteger.ONE;
            BigInteger denominator = BigInteger.ONE;

            int xi = shares.get(i).x;

            for (int j = 0; j < shares.size(); j++) {
                if (i == j) continue;

                int xj = shares.get(j).x;

                numerator = numerator.multiply(BigInteger.valueOf(-xj));
                denominator = denominator.multiply(BigInteger.valueOf(xi - xj));
            }

            BigInteger term = shares.get(i).y.multiply(numerator).divide(denominator);
            result = result.add(term);
        }

        return result;
    }
}